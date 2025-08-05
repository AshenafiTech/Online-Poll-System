
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.models import Poll, Choice, Vote
from polls.api.serializers import PollSerializer, ChoiceSerializer, VoteSerializer
from polls.api.permissions import IsPollCreatorOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@swagger_auto_schema(tags=['Polls'], operation_description="Manage polls: create, list, retrieve, update, delete.")
class PollViewSet(viewsets.ModelViewSet):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsPollCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Prevent changing created_by on update
        serializer.save(created_by=self.get_object().created_by)

    @swagger_auto_schema(
        method='post',
        operation_description="Vote or change your vote for a poll. Atomic and race-condition safe.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['choice'],
            properties={
                'choice': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the choice to vote for', example=1),
            },
            example={"choice": 1}
        ),
        responses={201: openapi.Response('Vote recorded'), 200: openapi.Response('Your vote has been updated'), 400: 'Bad request'},
        tags=['Polls', 'Voting']
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        from django.db import transaction
        poll = self.get_object()
        choice_id = request.data.get('choice')
        if not choice_id:
            return Response({'detail': 'Choice ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            choice = poll.choices.get(id=choice_id)
        except Choice.DoesNotExist:
            return Response({'detail': 'Invalid choice for this poll.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if poll is active and not expired
        from django.utils import timezone
        now = timezone.now()
        if not poll.is_active or (poll.expires_at and poll.expires_at < now):
            return Response({'detail': 'Voting is closed for this poll.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            vote, created = Vote.objects.select_for_update().get_or_create(
                poll=poll, user=request.user, defaults={'choice': choice}
            )
            if not created:
                vote.choice = choice
                vote.save()
                return Response({'detail': 'Your vote has been updated.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Vote recorded.'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method='get',
        operation_description="Get poll results (vote counts for each choice). Optimized with annotate.",
        responses={200: openapi.Response('Poll results')},
        tags=['Polls', 'Results']
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def results(self, request, pk=None):
        from django.db.models import Count
        poll = self.get_object()
        choices = poll.choices.annotate(votes=Count('vote'))
        results = [{'choice': c.text, 'votes': c.votes} for c in choices]
        return Response({'question': poll.question, 'results': results})


@swagger_auto_schema(tags=['Choices'], operation_description="Manage choices for polls.")
class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@swagger_auto_schema(tags=['Votes'], operation_description="View and manage votes.")
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
