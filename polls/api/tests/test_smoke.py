from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class EndpointSmokeTest(APITestCase):
    """
    Smoke test for all main API endpoints to ensure they respond (200/401/403/405/404).
    Add or adjust endpoints as your API evolves.
    """
    def setUp(self):
        self.client = APIClient()

    def test_poll_list(self):
        url = reverse('poll-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_poll_detail(self):
        # This will 404 if no poll exists, but endpoint is checked
        url = reverse('poll-detail', args=[1])
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403, 404])

    def test_options_list(self):
        url = reverse('option-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_votes_list(self):
        url = reverse('vote-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_guest_votes_list(self):
        url = reverse('guestvote-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_poll_analytics_list(self):
        url = reverse('pollview-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_user_registration(self):
        url = reverse('user-register')
        data = {'username': 'smoketest', 'password': 'testpass123', 'email': 'smoke@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [201, 400])

    def test_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'smoketest', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [200, 401, 400])

    def test_token_refresh(self):
        url = reverse('token_refresh')
        data = {'refresh': 'invalidtoken'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [200, 401, 400])
