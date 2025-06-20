from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import CustomerProfile
from store.models import Product, ProductVariation
from recommendation.engine import RecommendationEngine

class RecommendationEngineTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@example.com', password='testpass123')
        self.customer = CustomerProfile.objects.create(
            user=self.user,
            skin_type='oily',
            concerns='acne,oiliness',
            finish_preference='matte',
            texture_preference='liquid'
        )
        
        # Create test products
        self.product1 = Product.objects.create(
            name="Matte Foundation",
            brand="Brand A",
            price=29.99,
            quantity=10,
            skin_type='oily',
            tags='matte,oil_control,acne',
            finish='matte',
            texture='liquid'
        )
        ProductVariation.objects.create(
            product=self.product1,
            variation_code="MATTE-01",
            quantity=5,
            skin_tone='warm',
            surface_tones='medium'
        )
        
        self.product2 = Product.objects.create(
            name="Dewy Foundation",
            brand="Brand B",
            price=34.99,
            quantity=15,
            skin_type='dry',
            tags='dewy,hydrating',
            finish='dewy',
            texture='cream'
        )
        ProductVariation.objects.create(
            product=self.product2,
            variation_code="DEWY-01",
            quantity=10,
            skin_tone='cool',
            surface_tones='fair'
        )
        
    def test_content_based_scoring(self):
        engine = RecommendationEngine()
        products = Product.objects.all()
        scores = engine._content_based_score(self.customer, products)
        
        # Product 1 should score higher than Product 2 for this customer
        self.assertGreater(scores[0], scores[1])
        
    def test_rule_based_scoring(self):
        engine = RecommendationEngine()
        products = Product.objects.all()
        
        # Test with matching undertone/surface tone
        self.customer.undertone = 'warm'
        self.customer.surface_tone = 'medium'
        scores = engine._rule_based_score(self.customer, products)
        self.assertEqual(scores[0], 1.0)  # Should match product1
        self.assertEqual(scores[1], 0.0)  # Should not match product2
        
    def test_hybrid_recommendations(self):
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(self.customer, n=2)
        
        # Should return 2 recommendations
        self.assertEqual(len(recommendations), 2)
        
        # First product should be the better match
        self.assertEqual(recommendations[0].product, self.product1)
        self.assertGreater(recommendations[0].match_score, recommendations[1].match_score)