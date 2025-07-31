from polls.models import Poll, Choice, Vote
from rest_framework import serializers

class PollSerializer(serializers.ModelSerializer):
    is_currently_active = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = ('created_by',)
        extra_fields = ['is_currently_active']

    def get_is_currently_active(self, obj):
        return obj.is_currently_active

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
