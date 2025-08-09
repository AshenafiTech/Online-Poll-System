from django.contrib import admin
from .models import Poll, Option, Vote, GuestVote, PollView


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_by', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option_text', 'poll']
    list_filter = ['poll']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'selected_option', 'user', 'created_at']
    list_filter = ['created_at']


@admin.register(GuestVote)
class GuestVoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'selected_option', 'ip_address', 'created_at']
    list_filter = ['created_at']


@admin.register(PollView)
class PollViewAdmin(admin.ModelAdmin):
    list_display = ['poll', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
