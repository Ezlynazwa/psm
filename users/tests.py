from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import CustomerProfile

User = get_user_model()

class CustomerProfileModelTest(TestCase):
    def test_str_and_concerns_list(self):
        user = User.objects.create_user(username='testcp', password='pass')
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        # set concerns and save
        profile.concerns = 'dry,oil'
        profile.save()
        self.assertEqual(str(profile), "testcp's Profile")
        self.assertListEqual(profile.get_primary_concerns_list(), ['dry', 'oil'])

class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        self.homepage = reverse('store:homepage')

    def test_signup_creates_user_and_redirects(self):
        data = {
            'username': 'u1',
            'email': 'u1@example.com',
            'password1': 'Strong1!',
            'password2': 'Strong1!'
        }
        resp = self.client.post(self.signup_url, data)
        self.assertRedirects(resp, self.homepage)
        self.assertTrue(User.objects.filter(username='u1').exists())

    def test_login_redirects_based_on_role(self):
        # normal user
        User.objects.create_user(username='u2', password='pw')
        resp1 = self.client.post(self.login_url, {'username': 'u2', 'password': 'pw'})
        self.assertRedirects(resp1, self.homepage)
        # staff user
        User.objects.create_user(username='s2', password='pw', is_staff=True)
        resp2 = self.client.post(self.login_url, {'username': 's2', 'password': 'pw'})
        self.assertEqual(resp2.status_code, 302)
        self.assertNotEqual(resp2.url, self.homepage)

class UserProfileIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        # Anggap anda ada URL name 'users:profile_detail' & 'users:profile_edit'
        # yang menerima argumen username
        self.profile_detail_url = lambda username: reverse('users:profile_detail', args=[username])
        self.profile_edit_url   = lambda username: reverse('users:profile_edit',   args=[username])

    def test_full_signup_to_profile_flow(self):
        # 1) Signup
        signup_data = {
            'username':  'intuser',
            'email':     'int@example.com',
            'password1': 'ComplexP@ss1',
            'password2': 'ComplexP@ss1',
        }
        resp = self.client.post(self.signup_url, signup_data)
        # selepas signup, redirect ke homepage (anda dah test sebelum ini)
        self.assertEqual(resp.status_code, 302)

        # 2) Profil automatik tercipta
        user = User.objects.get(username='intuser')
        profile = CustomerProfile.objects.get(user=user)
        self.assertIsNotNone(profile)

        # 3) Login
        resp = self.client.post(self.login_url, {
            'username': 'intuser',
            'password': 'ComplexP@ss1'
        })
        self.assertEqual(resp.status_code, 302)

        # 4) Akses halaman detail profil
        resp = self.client.get(self.profile_detail_url('intuser'))
        self.assertEqual(resp.status_code, 200)
        # Pastikan tajuk profil dipaparkan
        self.assertContains(resp, "intuser's Profile")

    def test_profile_edit_updates_concerns_and_redirects(self):
        # Sediakan user & profile
        user = User.objects.create_user(username='edituser', password='Passw0rd!')
        profile, created = CustomerProfile.objects.get_or_create(user=user)
        self.client.login(username='edituser', password='Passw0rd!')

        # 1) Hantar form kemaskini profil
        edit_data = {
            'first_name': 'Edit',
            'last_name':  'User',
            'concerns':   'acne, redness',
        }
        resp = self.client.post(self.profile_edit_url('edituser'), edit_data)
        # anda boleh assertRedirects jika view redirect selepas berjaya
        self.assertEqual(resp.status_code, 302)

        # 2) Semak perubahan di database
        profile = CustomerProfile.objects.get(user__username='edituser')
        self.assertEqual(profile.first_name, 'Edit')
        self.assertEqual(profile.last_name,  'User')
        # get_primary_concerns_list() patut return ['acne','redness'] :contentReference[oaicite:0]{index=0}
        self.assertListEqual(profile.get_primary_concerns_list(), ['acne', 'redness'])

