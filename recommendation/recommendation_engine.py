import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brew_beauty.settings")
django.setup()
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from users.models import CustomerProfile 
from store.models import Product, ProductRecommendation, ProductVariation
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix, csr_matrix
import scipy.sparse as sp
from .models import RecommendationEvent

class CFRecommender:
    def __init__(self, factors=50, reg=0.01, iterations=15):
        self.factors = factors
        self.reg = reg
        self.iterations = iterations
        self.user_factors = None
        self.item_factors = None
        self.user_index = {}
        self.item_index = {}
        self.user_reverse = {}
        self.item_reverse = {}

    def build(self):
        # 1) Map users/items to matrix indices
        events = RecommendationEvent.objects.all()
        users = sorted({e.user_id for e in events})
        items = sorted({e.product_id for e in events})
        
        self.user_index = {u:i for i,u in enumerate(users)}
        self.item_index = {p:i for i,p in enumerate(items)}
        self.user_reverse = {i:u for u,i in self.user_index.items()}
        self.item_reverse = {i:p for p,i in self.item_index.items()}

        # 2) Build sparse matrix
        rows, cols, vals = [], [], []
        weight = {'view': 0.1, 'click': 0.3, 'purchase': 1.0}
        for e in events:
            ui = self.user_index[e.user_id]
            pi = self.item_index[e.product_id]
            rows.append(ui)
            cols.append(pi)
            vals.append(weight[e.event_type])
        
        R = coo_matrix((vals, (rows, cols)), shape=(len(users), len(items))).tocsr()
        
        # 3) Perform matrix factorization
        self.user_factors, self.item_factors = self._matrix_factorization(R)

    def _matrix_factorization(self, R):
        # Initialize factors randomly
        n_users, n_items = R.shape
        P = np.random.normal(scale=1./self.factors, size=(n_users, self.factors))
        Q = np.random.normal(scale=1./self.factors, size=(n_items, self.factors))

        # Perform gradient descent
        for _ in range(self.iterations):
            for i, j, r in zip(R.row, R.col, R.data):
                if r > 0:
                    eij = r - np.dot(P[i,:], Q[j,:].T)
                    P[i,:] += self.reg * (eij * Q[j,:] - self.reg * P[i,:])
                    Q[j,:] += self.reg * (eij * P[i,:] - self.reg * Q[j,:])
        
        return P, Q

    def recommend_for_user(self, user_id, N=5):
        ui = self.user_index.get(user_id)
        if ui is None or self.user_factors is None:
            return []
            
        # Calculate scores for all items
        user_vector = self.user_factors[ui]
        scores = np.dot(self.item_factors, user_vector)
        
        # Get top N items
        top_indices = np.argsort(scores)[::-1][:N]
        return [(self.item_reverse[i], float(scores[i])) for i in top_indices]
    
class MakeupRecommender:
    def __init__(self, content_weight=0.4, rule_weight=0.4, popularity_weight=0.2):
        self.w_content = content_weight
        self.w_rule = rule_weight
        self.w_popular = popularity_weight

        products = Product.objects.filter(quantity__gt=0).only(
            'id', 'name', 'detailed_description', 'tags'
        )
        self.prod_ids = []
        corpus = []
        for p in products:
            text = ' '.join(filter(None, [p.name, p.detailed_description, p.tags])).lower()
            self.prod_ids.append(p.id)
            corpus.append(text)

        if corpus:
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
            self.prod_tfidf = self.vectorizer.fit_transform(corpus)
        else:
            self.vectorizer = None
            self.prod_tfidf = None

    def recommend(self, customer_id, k=5):
        try:
            customer = CustomerProfile.objects.get(user_id=customer_id)
            assess = customer.skin_assessments.first() if customer.skin_assessments.exists() else None

            # Step 1: Scoring
            c_scores = self._content_scores(assess)
            r_scores = self._rule_scores(assess)
            p_scores = self._popularity_scores()

            # Step 2: Normalize
            c_norm = self._normalize(c_scores)
            r_norm = self._normalize(r_scores)
            p_norm = self._normalize(p_scores)
            all_ids = set(c_norm) | set(r_norm) | set(p_norm)

            # Step 3: Blend scores
            final = {
                pid: self.w_content * c_norm.get(pid, 0.0) +
                     self.w_rule * r_norm.get(pid, 0.0) +
                     self.w_popular * p_norm.get(pid, 0.0)
                for pid in all_ids
            }

            # Step 4: Add fallback if not enough
            if len(final) < k:
                fallback = Product.objects.filter(quantity__gt=0).exclude(id__in=final.keys())\
                    .order_by('-popularity_score')[:k - len(final)]
                for p in fallback:
                    final[p.id] = 0.5

            # Step 5: Sort and select top
            top = sorted(final.items(), key=lambda x: x[1], reverse=True)[:k]

            # Step 6: Save to DB
            ProductRecommendation.objects.filter(customer=customer).delete()
            for pid, score in top:
                reason = f"Match Score: {score:.2f}"
                ProductRecommendation.objects.create(
                    customer=customer,
                    product_id=pid,
                    match_score=score,
                    reason=reason
                )

            return top

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in recommend(): {e}")

            fallback = Product.objects.filter(quantity__gt=0).order_by('-popularity_score')[:k]
            return [(p.id, 0.5) for p in fallback]

    def _normalize(self, scores):
        if not scores:
            return {}
        m = max(scores.values()) or 1.0
        return {pid: score / m for pid, score in scores.items()}

    def _content_scores(self, assess):
        if not self.vectorizer or self.prod_tfidf is None:
            return {}
        user_tokens = []
        if assess:
            user_tokens = [assess.skin_type or '', assess.finish_preference or '', assess.texture_preference or '']
            if assess.concerns:
                user_tokens += assess.concerns.split(',')
        user_text = ' '.join(token for token in user_tokens if token).lower()
        if not user_text:
            return {}
        vec = self.vectorizer.transform([user_text])
        sims = cosine_similarity(vec, self.prod_tfidf).flatten()
        return {self.prod_ids[i]: float(sims[i]) for i in range(len(sims)) if sims[i] > 0}

    def _rule_scores(self, assess):
        scores = {}
        products = Product.objects.filter(quantity__gt=0).only(
            'id', 'finish', 'texture', 'is_hypoallergenic', 'skin_condition', 'spf'
        )
        for p in products:
            score = 0.0
            if assess and assess.sensitivity_level >= 4 and not p.is_hypoallergenic:
                score -= 0.3
            if assess and assess.sensitivity_level >= 4:
                score += 0.6
            if assess and assess.oiliness_level >= 4:
                score += 0.5 * (p.finish == 'matte') + 0.3 * (p.texture == 'powder')
            if assess and assess.hydration_level <= 2:
                score += 0.5 * (p.finish == 'dewy') + 0.3 * (p.texture in ['cream', 'liquid'])
            if assess and assess.acne_proneness >= 4:
                tags = set((p.skin_condition or '').split(','))
                if {'oil', 'mineral_oil', 'lanolin'} & tags:
                    continue
                score += 0.4 * ('non_comedogenic' in tags)
            if assess and assess.aging_concerns >= 3:
                tags = set((p.skin_condition or '').split(','))
                score += 0.4 * bool({'anti_aging', 'hydrating'} & tags)
            score += 0.1 * ((p.spf or 0) >= 15)
            shade_ok = ProductVariation.objects.filter(
                product_id=p.id,
                skin_tone=assess.undertone if assess else None,
                surface_tones=assess.surface_tone if assess else None
            ).exists()
            if not shade_ok:
                score -= 0.2
            if score > 0:
                scores[p.id] = score
        return scores

    def _popularity_scores(self):
        qs = Product.objects.filter(quantity__gt=0).only('id', 'popularity_score')
        maxp = max((p.popularity_score or 0) for p in qs) or 1
        return {p.id: (p.popularity_score or 0) / maxp for p in qs}
    
class EvaluationPipeline:
    def __init__(self):
        qs = ProductRecommendation.objects.values('customer__user_id','product_id')
        self.df = pd.DataFrame(list(qs)).rename(columns={'customer__user_id':'user_id','product_id':'product_id'})
    def train_test_split(self, test_size=0.2, random_state=42):
        return train_test_split(self.df, test_size=test_size, random_state=random_state)
    def precision_at_k(self, model, df, k=5):
        return np.mean([len({pid for pid,_ in model.recommend(u,k)} & set(group['product_id']))/k 
            for u,group in df.groupby('user_id')])
    def recall_at_k(self, model, df, k=5):
        return np.mean([len({pid for pid,_ in model.recommend(u,k)} & set(group['product_id']))/len(set(group['product_id'])) 
            for u,group in df.groupby('user_id')])


class SklearnRecommender:
    def __init__(self, vectorizer:TfidfVectorizer, n_neighbors:int=5):
        self.vec = vectorizer
        self.n = n_neighbors
    def build(self):
        products = list(Product.objects.filter(quantity__gt=0))
        texts = [f"{p.name} {p.tags or ''}" for p in products]
        mat = self.vec.fit_transform(texts).toarray().astype(np.float32)
        self.nn = NearestNeighbors(n_neighbors=self.n+1,metric='cosine').fit(mat)
        self.id_map = {i:p.id for i,p in enumerate(products)}
        self.mat = mat
    def recommend(self, user_id, k=5):
        return []  # placeholder for integration

class EpsilonGreedyRecommender:
    def __init__(self, base, epsilon:float=0.1): self.base, self.epsilon = base, epsilon
    def recommend(self, u,k=5):
        recs = self.base.recommend(u,k)
        if random.random()<self.epsilon:
            pid = random.choice(list(self.id_map.values()))
            recs[-1] = (pid,0)
        return recs



def initialize_services():
    # 1) Content‐based (sklearn TF-IDF nearest neighbors)
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    skl = SklearnRecommender(vectorizer=tfidf, n_neighbors=5)
    skl.build()

    # 2) Collaborative‐filtering (ALS)
    cf = CFRecommender(factors=64, reg=0.05)
    cf.build()

    # 3) Base hybrid (your existing C/R/P recommender)
    base_hybrid = MakeupRecommender(
        content_weight=0.50,
        rule_weight=0.25,
        popularity_weight=0.25
    )

    # 4) Extended hybrid = base_hybrid + CF
    extended = ExtendedHybridRecommender(
        base_hybrid=base_hybrid,
        cf_model=cf,
        w_cf=0.10         # tune this via tune_recs
    )

    # 5) Wrap in ε-greedy exploration
    explorer = EpsilonGreedyRecommender(extended, epsilon=0.05)

    # 6) Return everything you’ll need
    return {
        'content_rec': skl,
        'cf_rec': cf,
        'base_hybrid': base_hybrid,
        'extended_hybrid': extended,
        'explorer': explorer,
    }


class ExtendedHybridRecommender:
    """
    Wraps your existing MakeupRecommender to also blend in CF scores.
    """
    def __init__(self, base_hybrid, cf_model, w_cf: float = 0.1):
        self.base = base_hybrid
        self.cf = cf_model
        self.w_cf = w_cf

    def recommend(self, user_id, k=5):
        # 1) get your hybrid (c/r/p) scores
        hybrid_list = self.base.recommend(user_id, k)
        hybrid_dict = {pid: score for pid, score in hybrid_list}

        # 2) get CF scores
        cf_list = self.cf.recommend_for_user(user_id, k)
        cf_dict = {pid: score for pid, score in cf_list}

        # 3) normalize
        max_h = max(hybrid_dict.values()) if hybrid_dict else 1.0
        max_cf = max(cf_dict.values()) if cf_dict else 1.0

        # 4) blend and rank
        final = []
        all_ids = set(hybrid_dict) | set(cf_dict)
        for pid in all_ids:
            h = hybrid_dict.get(pid, 0.0) / max_h
            c = cf_dict.get(pid, 0.0) / max_cf
            # you can decide if you want to re‐weight the original hybrid total,
            # or treat h as already the blend of c/r/p. Here we just mix hybrid vs CF:
            score = (1 - self.w_cf) * h + self.w_cf * c
            final.append((pid, score))

        final.sort(key=lambda x: x[1], reverse=True)
        return final[:k]


def run_evaluation():
    ep = EvaluationPipeline()
    tr,te = ep.train_test_split()
    _,_,ex = initialize_services()
    print("P@5", ep.precision_at_k(ex,te))
    print("R@5", ep.recall_at_k(ex,te))

class HybridRecommender:
    """Combines content-based, collaborative filtering, and rule-based recommendations"""
    def __init__(self, content_weight=0.4, cf_weight=0.3, rule_weight=0.3):
        self.content_weight = content_weight
        self.cf_weight = cf_weight
        self.rule_weight = rule_weight
        self.content_model = MakeupRecommender()
        self.cf_model = CFRecommender()
        self.cf_model.build()

        
    def recommend(self, user_id, k=5):
        try:
            # Get content-based recommendations
            content_recs = self.content_model.recommend(user_id, k*3)  # Get more for blending
            
            # Get collaborative filtering recommendations
            cf_recs = self.cf_model.recommend_for_user(user_id, k*3)
            
            # Combine scores
            combined = {}
            for pid, score in content_recs:
                combined[pid] = combined.get(pid, 0) + score * self.content_weight
                
            for pid, score in cf_recs:
                combined[pid] = combined.get(pid, 0) + score * self.cf_weight
                
            # Apply rule-based filtering
            customer = CustomerProfile.objects.get(user_id=user_id)
            assessment = customer.skin_assessments.first() if customer.skin_assessments.exists() else None
            valid_products = self._filter_by_rules(assessment, combined.keys())
            
            # Final scoring
            final_scores = {pid: score for pid, score in combined.items() if pid in valid_products}
            
            return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:k]
            
        except Exception as e:
            # Fallback to popular products if error occurs
            popular = Product.objects.filter(quantity__gt=0).order_by('-popularity_score')[:k]
            return [(p.id, 0.8) for p in popular]

    def _filter_by_rules(self, assessment, product_ids):
        # Implement rule-based filtering based on skin assessment
        products = Product.objects.filter(id__in=product_ids)
        valid_ids = set()
        
        for product in products:
            if self._is_product_compatible(assessment, product):
                valid_ids.add(product.id)
                
        return valid_ids

    def _is_product_compatible(self, assessment, product):
        # Implement compatibility rules based on assessment
        if not assessment:
            return True
            
        # Example rule: Filter out non-hypoallergenic products for sensitive skin
        if assessment.sensitivity_level >= 4 and not product.is_hypoallergenic:
            return False
            
        # Add more rules as needed
        return True
