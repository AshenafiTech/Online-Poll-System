from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from polls.models import Poll, Option, Vote, GuestVote

User = get_user_model()

class PollAPITests(APITestCase):
    def setUp(self):
        import os
        test_password = os.environ.get('TEST_PASSWORD', 'secure_test_password_123')
        self.user = User.objects.create_user(username='testuser', password=test_password)
        self.other_user = User.objects.create_user(username='otheruser', password=test_password)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.other_client = APIClient()
        self.other_client.force_authenticate(user=self.other_user)
        self.guest_client = APIClient()
        self.poll = Poll.objects.create(question='Favorite color?', created_by=self.user)
        self.option1 = Option.objects.create(poll=self.poll, option_text='Red')
        self.option2 = Option.objects.create(poll=self.poll, option_text='Blue')

    def test_create_poll(self):
        url = reverse('poll-list')
        data = {
            'question': 'Best animal?',
            'is_active': True,
            'options_data': ['Dog', 'Cat', 'Bird']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)

    def test_create_poll_requires_auth(self):
        url = reverse('poll-list')
        data = {
            'question': 'Unauthorized?',
            'is_active': True,
            'options_data': ['A', 'B']
        }
        response = self.guest_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_polls(self):
        url = reverse('poll-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_authenticated_vote(self):
        url = reverse('poll-vote', args=[self.poll.id])
        response = self.client.post(url, {'option': self.option1.id}, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertEqual(Vote.objects.filter(poll=self.poll, user=self.user).count(), 1)

    def test_authenticated_vote_update(self):
        url = reverse('poll-vote', args=[self.poll.id])
        # First vote
        self.client.post(url, {'option': self.option1.id}, format='json')
        # Change vote
        response = self.client.post(url, {'option': self.option2.id}, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        vote = Vote.objects.get(poll=self.poll, user=self.user)
        self.assertEqual(vote.selected_option, self.option2)

    def test_guest_vote(self):
        url = reverse('poll-vote', args=[self.poll.id])
        session_id = 'guest-session-1'
        ip_address = '1.2.3.4'
        self.guest_client.cookies['sessionid'] = session_id
        response = self.guest_client.post(url, {'option': self.option1.id}, REMOTE_ADDR=ip_address, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertEqual(GuestVote.objects.filter(poll=self.poll, session_id=session_id, ip_address=ip_address).count(), 1)

    def test_close_poll_by_creator(self):
        url = reverse('poll-close', args=[self.poll.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK])
        self.poll.refresh_from_db()
        self.assertFalse(self.poll.is_active)

    def test_close_poll_by_non_creator(self):
        url = reverse('poll-close', args=[self.poll.id])
        response = self.other_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reopen_poll_by_creator(self):
        # First close the poll
        self.poll.is_active = False
        self.poll.save()
        url = reverse('poll-reopen', args=[self.poll.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK])
        self.poll.refresh_from_db()
        self.assertTrue(self.poll.is_active)

    def test_reopen_poll_by_non_creator(self):
        self.poll.is_active = False
        self.poll.save()
        url = reverse('poll-reopen', args=[self.poll.id])
        response = self.other_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_poll_results(self):
        url = reverse('poll-results', args=[self.poll.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('question', response.data)
        self.assertIn('results', response.data)

    def test_poll_analytics_list(self):
        url = reverse('pollview-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN])

    def test_invalid_option_vote(self):
        url = reverse('poll-vote', args=[self.poll.id])
        response = self.client.post(url, {'option': 9999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_on_closed_poll(self):
        self.poll.is_active = False
        self.poll.save()
        url = reverse('poll-vote', args=[self.poll.id])
        response = self.client.post(url, {'option': self.option1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
