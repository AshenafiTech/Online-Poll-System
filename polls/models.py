from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, db_index=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('poll', 'user'),)  # One vote per user per poll

    def __str__(self):
        return f"{self.user} voted {self.choice} on {self.poll}"
