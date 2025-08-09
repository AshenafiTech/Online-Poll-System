from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from polls.models import Poll, Option, Vote, GuestVote, PollView
from polls.api.serializers.poll import PollSerializer, OptionSerializer, VoteSerializer, GuestVoteSerializer, PollViewSerializer
from polls.api.permissions.permissions import IsPollCreatorOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GuestVoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Guest Votes
    
    Manage votes from unauthenticated users.
    """
    queryset = GuestVote.objects.select_related('poll', 'selected_option')
    serializer_class = GuestVoteSerializer
    permission_classes = [permissions.AllowAny]

class PollAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Poll Analytics
    
    Track poll view statistics and analytics.
    """
    @swagger_auto_schema(auto_schema=None, tags=["Poll Analytics"])
    def list(self, request, *args, **kwargs):
        """List poll analytics data."""
        return super().list(request, *args, **kwargs)
    queryset = PollView.objects.select_related('poll', 'user')
    serializer_class = PollViewSerializer
    permission_classes = [permissions.AllowAny]

class PollViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        method='post',
        operation_summary="Reopen Poll",
        operation_description=(
            "Reopen a closed poll. Only the poll creator can perform this action. "
            "Sets is_active to True.\n\n"
            "**Permissions:** Only the poll creator can reopen.\n\n"
            "**Responses:**\n"
            "- 200: Poll reopened successfully.\n"
            "- 400: Poll is already open.\n"
            "- 403: You do not have permission to reopen this poll."
        ),
        responses={
            200: openapi.Response(
                description='Poll reopened successfully.',
                examples={
                    'application/json': {'detail': 'Poll reopened successfully.'}
                }
            ),
            400: openapi.Response(
                description='Poll is already open.',
                examples={
                    'application/json': {'detail': 'Poll is already open.'}
                }
            ),
            403: openapi.Response(
                description='You do not have permission to reopen this poll.',
                examples={
                    'application/json': {'detail': 'You do not have permission to reopen this poll.'}
                }
            )
        },
        tags=['Polls Management']
    )
    @action(detail=True, methods=['post'], permission_classes=[IsPollCreatorOrReadOnly])
    def reopen(self, request, pk=None):
        """
        Reopen a closed poll (reactivate voting).\n\n
        **Who can use:** Only the poll creator.\n
        **What it does:** Sets `is_active` to True, allowing users to vote again.\n
        **Returns:**
        - 200: Poll reopened successfully.
        - 400: Poll is already open.
        - 403: You do not have permission to reopen this poll.
        """
        poll = self.get_object()
        if not request.user.is_authenticated or poll.created_by != request.user:
            return Response({'detail': 'You do not have permission to reopen this poll.'}, status=status.HTTP_403_FORBIDDEN)
        if poll.is_active:
            return Response({'detail': 'Poll is already open.'}, status=status.HTTP_400_BAD_REQUEST)
        poll.is_active = True
        poll.save()
        return Response({'detail': 'Poll reopened successfully.'}, status=status.HTTP_200_OK)
    """
    ViewSet for managing polls.
    - Create, view, update, and delete polls.
    - Only poll creators can modify or close their polls.
    - Voting and results endpoints are provided as custom actions.
    """
    @swagger_auto_schema(
        method='post',
        operation_summary="Close Poll",
        operation_description=(
            "Close (deactivate) a poll. Only the poll creator can perform this action. "
            "Sets is_active to False.\n\n"
            "**Permissions:** Only the poll creator can close.\n\n"
            "**Responses:**\n"
            "- 200: Poll closed successfully.\n"
            "- 403: You do not have permission to close this poll."
        ),
        responses={
            200: openapi.Response(
                description='Poll closed successfully.',
                examples={
                    'application/json': {'detail': 'Poll closed successfully.'}
                }
            ),
            403: openapi.Response(
                description='You do not have permission to close this poll.',
                examples={
                    'application/json': {'detail': 'You do not have permission to close this poll.'}
                }
            )
        },
        tags=['Polls Management']
    )
    @action(detail=True, methods=['post'], permission_classes=[IsPollCreatorOrReadOnly])
    def close(self, request, pk=None):
        """
        Close a poll (deactivate voting).\n\n
        **Who can use:** Only the poll creator.\n
        **What it does:** Sets `is_active` to False, preventing further votes.\n
        **Returns:**
        - 200: Poll closed successfully.
        - 403: You do not have permission to close this poll.
        """
        poll = self.get_object()
        if not request.user.is_authenticated or poll.created_by != request.user:
            return Response({'detail': 'You do not have permission to close this poll.'}, status=status.HTTP_403_FORBIDDEN)
        poll.is_active = False
        poll.save()
        return Response({'detail': 'Poll closed successfully.'}, status=status.HTTP_200_OK)
    """
    Polls Management
    
    Create, view, update and delete polls. Authentication required for creating polls.
    Poll creators can modify their own polls, others can only view.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsPollCreatorOrReadOnly]
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(created_by=self.get_object().created_by)

    @swagger_auto_schema(
        method='post',
        operation_summary="Vote on Poll",
        operation_description="Submit or update your vote for a specific poll. Supports both authenticated users and guests.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['option'],
            properties={
                'option': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description='ID of the option to vote for',
                    example=1
                ),
            }
        ),
        responses={
            201: openapi.Response('Vote successfully recorded'),
            200: openapi.Response('Vote successfully updated'),
            400: openapi.Response('Bad request - invalid option or missing data'),
            401: openapi.Response('Authentication required for some polls')
        },
        tags=['Voting']
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def vote(self, request, pk=None):
        """
        Custom action to vote on a poll.
        Accepts option ID in the request body. Handles both authenticated and guest voting.
        Voting is only allowed if the poll is active and not expired.
        """
        from django.db import transaction
        from django.utils import timezone
        poll = self.get_object()
        option_id = request.data.get('option')
        if not option_id:
            return Response({'detail': 'Option ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            option = poll.options.get(id=option_id)
        except Option.DoesNotExist:
            return Response({'detail': 'Invalid option for this poll.'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        if not poll.is_active or (poll.expires_at and poll.expires_at < now):
            return Response({'detail': 'Voting is closed for this poll.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None
        session_id = request.session.session_key or request.COOKIES.get('sessionid') or request.data.get('session_id')
        ip_address = request.META.get('REMOTE_ADDR')

        if user:
            with transaction.atomic():
                vote, created = Vote.objects.select_for_update().get_or_create(
                    poll=poll, user=user, defaults={'selected_option': option, 'session_id': session_id, 'ip_address': ip_address}
                )
                if not created:
                    vote.selected_option = option
                    vote.save()
                    return Response({'detail': 'Your vote has been updated.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Vote recorded.'}, status=status.HTTP_201_CREATED)
        else:
            if not session_id or not ip_address:
                return Response({'detail': 'Session ID and IP address are required for guest voting.'}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                guest_vote, created = GuestVote.objects.select_for_update().get_or_create(
                    poll=poll, session_id=session_id, ip_address=ip_address, defaults={'selected_option': option}
                )
                if not created:
                    guest_vote.selected_option = option
                    guest_vote.save()
                    return Response({'detail': 'Your vote has been updated (guest).'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Vote recorded (guest).'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method='get',
        operation_summary="Get Poll Results",
        operation_description="Retrieve vote counts and statistics for all options in a poll.",
        responses={
            200: openapi.Response(
                'Poll results with vote counts',
                examples={
                    'application/json': {
                        'question': 'Favorite Programming Language',
                        'results': [
                            {'option': 'Python', 'votes': 15},
                            {'option': 'JavaScript', 'votes': 8}
                        ]
                    }
                }
            ),
            404: openapi.Response('Poll not found')
        },
        tags=['Results']
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def results(self, request, pk=None):
        """
        Custom action to retrieve poll results (vote counts for each option).
        Returns the poll question and a list of options with their total votes.
        """
        from django.db.models import Count, Q
        poll = self.get_object()
        
        # Optimized single query with aggregation
        results = poll.options.annotate(
            vote_count=Count('vote', distinct=True),
            guest_vote_count=Count('guestvote', distinct=True)
        ).values('option_text', 'vote_count', 'guest_vote_count')
        
        formatted_results = [
            {
                'option': result['option_text'],
                'votes': result['vote_count'] + result['guest_vote_count']
            }
            for result in results
        ]
        
        return Response({'question': poll.question, 'results': formatted_results})

class OptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing poll options (choices).
    - List, create, update, and delete options for polls.
    - Only authenticated users can create, update, or delete options.
    - Anyone can view options.
    """
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing authenticated user votes.
    - List, create, update, and delete votes for authenticated users.
    - Only authenticated users can create, update, or delete votes.
    - Anyone can view votes (if allowed by permissions).
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
