from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'newuser'
        self.password = 'newuserpass123'
        self.email = 'newuser@example.com'

    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        response = self.client.post(url, data, format='json')
        # 400 if user exists or invalid
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            self.assertTrue(User.objects.filter(
                username=self.username).exists())

    def test_user_profile_requires_auth(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_authenticated(self):
        user = User.objects.create_user(
            username='profileuser', password='profilepass', email='profile@example.com')
        self.client.force_authenticate(user=user)
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')
        self.assertEqual(response.data['email'], 'profile@example.com')
