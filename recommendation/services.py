# recommendation/services.py

from django.core.cache import cache

# Import from the apps where these models actually live:
from users.models import CustomerProfile
from store.models import ProductRecommendation

from .engine import MakeupRecommender


class RecommendationService:
    """
    Fetches (or recomputes) recommendations for a given CustomerProfile.
    Caches them in Redis for 30 minutes and persists them into ProductRecommendation.
    """

    def __init__(self):
        self.engine = MakeupRecommender(
            content_weight=0.4, rule_weight=0.4, popularity_weight=0.2
        )

    def get_for_customer(self, customer: CustomerProfile, top_n=10):

        cache_key = f"makeup_recs_{customer.id}"
        recs = cache.get(cache_key)
        if recs is not None:
            return recs

        # 1) Compute fresh recommendations
        recs = self.engine.get_recommendations(customer, top_n=top_n)

        # 2) Persist into ProductRecommendation (so we can analyze later)
        #    Must delete any existing rows first to avoid unique_together collisions
        ProductRecommendation.objects.filter(customer=customer).delete()
        objs = []
        for rec in recs:
            objs.append(
                ProductRecommendation(
                    product=rec["product"],
                    customer=customer,
                    match_score=rec["combined_score"],
                    reason=rec["reason"],
                )
            )
        ProductRecommendation.objects.bulk_create(objs)

        # 3) Cache the list of dicts (serializable)
        cache.set(cache_key, recs, 60 * 30)  # 30 minutes

        return recs

    def invalidate_cache_for_customer(self, customer_id):
        cache_key = f"makeup_recs_{customer_id}"
        cache.delete(cache_key)
