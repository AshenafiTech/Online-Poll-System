from django.contrib.auth.models import User
from rest_framework import generics, permissions
from polls.api.serializers.user import UserProfileSerializer


from drf_yasg.utils import swagger_auto_schema

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User Profile
    
    View and update your user profile information. Authentication required.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get user profile",
        operation_description="Retrieve the authenticated user's profile information.",
        tags=["Users"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Update the authenticated user's profile information.",
        tags=["Users"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
