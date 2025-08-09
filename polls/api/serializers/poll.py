from rest_framework import serializers
from polls.models import Poll, Option, Vote, GuestVote, PollView
from django.utils import timezone
from django.utils.html import escape


class OptionSerializer(serializers.ModelSerializer):
    """
    Serializer for poll options (choices).
    """
    class Meta:
        model = Option
        fields = ['id', 'option_text']


class PollSerializer(serializers.ModelSerializer):
    """
    Serializer for Polls. Requires at least two unique options at creation.
    - question: The poll question (string).
    - expires_at: Optional expiration datetime (ISO 8601).
    - is_active: Whether the poll is open for voting.
    - options_data: List of option texts (choices) to create with the poll.
    - options: List of created options (read-only).
    - created_at: Poll creation timestamp (read-only).
    """

    def validate_options_data(self, value):
        # Ensure all option texts are unique (case-insensitive)
        normalized = [opt.strip().lower() for opt in value]
        if len(normalized) != len(set(normalized)):
            raise serializers.ValidationError(
                "All option texts must be unique.")
        return value
    options_data = serializers.ListField(
        child=serializers.CharField(
            max_length=255, help_text="Text for a poll option (choice)."),
        write_only=True,
        required=True,
        min_length=2,
        help_text="Provide at least two unique options for the poll."
    )
    question = serializers.CharField(help_text="The poll question.")
    expires_at = serializers.DateTimeField(
        required=False, allow_null=True, help_text="Optional expiration date/time (ISO 8601). Null means no expiry.")
    is_active = serializers.BooleanField(
        default=True, required=False, help_text="Is the poll open for voting? Defaults to True.")
    options = OptionSerializer(
        many=True, read_only=True, help_text="List of poll options (choices). Read-only.")
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Poll creation timestamp.")
    options = OptionSerializer(many=True, read_only=True)

    expires_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'expires_at', 'is_active',
                  'options', 'options_data', 'created_at']
        read_only_fields = ('created_by', 'created_at')

    def validate_question(self, value):
        return escape(value)

    def create(self, validated_data):
        options_data = validated_data.pop('options_data')
        poll = Poll.objects.create(**validated_data)
        for option_text in options_data:
            Option.objects.create(poll=poll, option_text=escape(option_text))
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class GuestVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestVote
        fields = '__all__'


class PollViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollView
        fields = '__all__'
