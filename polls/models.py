
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    allow_multiple_votes = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('poll', 'user'),)

class GuestVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45)
    session_id = models.CharField(max_length=255)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('poll', 'ip_address', 'session_id'),)

class PollView(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
