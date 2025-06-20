import json
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from unittest.mock import patch

from django.contrib.auth import get_user_model
from users.models import CustomerProfile
from store.models import Product
from recommendation.views import dashboard, api_recommendations
from recommendation.forms import SkinAssessmentForm
from recommendation.models import SkinAssessment

User = get_user_model()

class RecommendationDashboardViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create user and associated profile
        self.user = User.objects.create_user(username='testuser', password='pass')
        CustomerProfile.objects.get_or_create(user=self.user)

    def _add_messages_middleware(self, request):
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_dashboard_redirects_if_no_assessment(self):
        request = self.factory.get('/')
        request.user = self.user
        self._add_messages_middleware(request)

        response = dashboard(request)
        self.assertEqual(response.status_code, 302)

    @patch('recommendation.views.RecommendationService')
    def test_dashboard_shows_recommendations(self, mock_service):
        # create skin assessment for user
        profile, _ = CustomerProfile.objects.get_or_create(user=self.user)
        SkinAssessment.objects.create(
            customer=profile,
            skin_type='normal', undertone='cool', concerns='',
            hydration_level=3, oiliness_level=3, sensitivity_level=3,
            acne_proneness=1, aging_concerns=1,
            finish_preference='', texture_preference=''
        )
        # mock recommendations
        prod = Product.objects.create(name='P', brand='B', size='10ml', price=1, quantity=1)
        fake_recs = [{'product': prod, 'combined_score': 0.5, 'reason': 'Reason'}]
        mock_service.return_value.get_for_customer.return_value = fake_recs

        request = self.factory.get('/')
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'P', response.content)

class SkinAssessmentFormTests(TestCase):
    def test_clean_and_save_concerns(self):
        # prepare form data
        data = {
            'skin_type': 'normal',
            'undertone': 'cool',
            'concerns': ['acne', 'redness'],
            'hydration_level': 3,
            'oiliness_level': 3,
            'sensitivity_level': 2,
            'acne_proneness': 1,
            'aging_concerns': 1,
            'finish_preference': '',
            'texture_preference': ''
        }
        form = SkinAssessmentForm(data=data)
        self.assertTrue(form.is_valid())
        inst = form.save(commit=False)
        # assign profile using get_or_create
        user = User.objects.create_user(username='u2', password='pass')
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        inst.customer = profile
        inst.save()
        self.assertEqual(inst.concerns, 'acne,redness')

class ApiRecommendationsViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # create user and profile
        self.user = User.objects.create_user(username='apiuser', password='pass')
        CustomerProfile.objects.get_or_create(user=self.user)

    @patch('recommendation.views.RecommendationService')
    def test_api_recommendations_success(self, mock_service):
        # prepare fake data
        prod = Product.objects.create(name='X', brand='Y', size='5ml', price=2, quantity=1)
        fake_recs = [{'product': prod, 'combined_score': 0.7, 'reason': 'Test'}]
        mock_service.return_value.get_for_customer.return_value = fake_recs

        request = self.factory.get('/')
        request.user = self.user
        response = api_recommendations(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['recommendations']), 1)
        rec = data['recommendations'][0]
        self.assertEqual(rec['product_id'], prod.id)
        self.assertEqual(rec['combined_score'], 0.7)

    @patch('recommendation.views.RecommendationService')
    def test_api_recommendations_error(self, mock_service):
        # simulate service failure
        mock_service.return_value.get_for_customer.side_effect = Exception('fail')

        request = self.factory.get('/')
        request.user = self.user
        response = api_recommendations(request)
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
