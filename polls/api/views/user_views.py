from django.contrib.auth.models import User
from rest_framework import generics, permissions, status

from rest_framework.response import Response
from polls.api.serializers.user import UserRegistrationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    """
    User Registration
    
    Register a new user account. No authentication required.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user account. No authentication required.",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={
                    'application/json': {'id': 1, 'username': 'newuser', 'email': 'user@example.com'}
                }
            ),
            400: openapi.Response(
                description="Validation error.",
                examples={
                    'application/json': {'username': ['This field is required.']}
                }
            )
        },
        tags=["Users"]
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'id': user.id, 'username': user.username, 'email': user.email},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
