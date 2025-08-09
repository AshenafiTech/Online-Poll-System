from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Poll(models.Model):
    question = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)
    allow_multiple_votes = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_polls')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        from django.utils.html import escape
        return escape(self.question)


class Option(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        from django.utils.html import escape
        return escape(self.option_text)


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('poll', 'user'),  # One vote per user per poll
            ('poll', 'session_id', 'ip_address'),  # One vote per guest per poll
        )
        indexes = [
            models.Index(fields=['poll', 'user']),
            models.Index(fields=['poll', 'selected_option']),
            models.Index(fields=['session_id', 'ip_address']),
        ]

    def __str__(self):
        from django.utils.html import escape
        if self.user:
            return f"{escape(str(self.user))} voted {escape(str(self.selected_option))} on {escape(str(self.poll))}"
        return f"Guest {escape(str(self.ip_address or self.session_id))} voted {escape(str(self.selected_option))} on {escape(str(self.poll))}"


# Optionally, if you want a separate GuestVote model (as in docs):
class GuestVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('poll', 'ip_address', 'session_id'),)


class PollView(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
