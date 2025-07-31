
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Poll, Choice, Vote

User = get_user_model()

class PollAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_poll(self):
        url = reverse('poll-list')
        data = {
            'question': 'Favorite color?',
            'expires_at': '2099-12-31T23:59:59Z',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 1)

    def test_list_polls(self):
        Poll.objects.create(question='Q1', created_by=self.user)
        url = reverse('poll-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_vote_on_poll(self):
        poll = Poll.objects.create(question='Q2', created_by=self.user)
        choice = Choice.objects.create(poll=poll, text='Option 1')
        url = reverse('poll-vote', args=[poll.id])
        response = self.client.post(url, {'choice': choice.id}, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertEqual(Vote.objects.filter(poll=poll, user=self.user).count(), 1)

    def test_profile_view(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
