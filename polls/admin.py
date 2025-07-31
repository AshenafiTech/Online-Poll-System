# Register your models here.

from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question', 'created_by', 'created_at', 'expires_at', 'is_active', 'current_status', 'vote_count')
    search_fields = ('question',)

    def vote_count(self, obj):
        return obj.vote_set.count()
    vote_count.short_description = 'Votes'

    def current_status(self, obj):
        return 'Active' if obj.is_currently_active else 'Closed'
    current_status.short_description = 'Status'

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll')
    search_fields = ('text',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'user', 'voted_at')
    search_fields = ('poll__question', 'user__username')
