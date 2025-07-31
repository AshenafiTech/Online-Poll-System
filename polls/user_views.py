"""
This file is now deprecated. User registration view has been moved to polls/api/user_views.py.
"""
from rest_framework import generics, permissions
from .user_serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .user_serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
