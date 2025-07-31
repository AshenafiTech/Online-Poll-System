"""
This file is now deprecated. User profile view has been moved to polls/api/user_profile.py.
"""
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'username', 'email')

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
