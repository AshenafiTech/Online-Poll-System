"""
This file is now deprecated. All serializers have been moved to polls/api/serializers.py.
"""
from rest_framework import serializers
from .models import Poll, Choice, Vote
from rest_framework import serializers
from .models import Poll, Choice, Vote

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
