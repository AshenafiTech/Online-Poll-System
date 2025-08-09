from drf_yasg.views import get_schema_view
from .views.user_profile import UserProfileView
from .views.user_views import UserRegistrationView
from .views.viewsets import PollViewSet, OptionViewSet, VoteViewSet, GuestVoteViewSet, PollAnalyticsViewSet
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom schema views for JWT endpoints


class TokenObtainPairViewPatched(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary="Obtain JWT token pair",
        operation_description="Obtain access and refresh tokens by providing username and password.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="user1"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, example="yourpassword")
            }
        ),
        responses={
            200: openapi.Response(
                description="JWT token pair",
                examples={
                    "application/json": {"refresh": "<refresh>", "access": "<access>"}
                }
            ),
            401: openapi.Response(description="Invalid credentials")
        },
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshViewPatched(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh JWT access token",
        operation_description="Obtain a new access token by providing a valid refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="<refresh>")
            }
        ),
        responses={
            200: openapi.Response(
                description="New access token",
                examples={
                    "application/json": {"access": "<access>"}
                }
            ),
            401: openapi.Response(description="Invalid refresh token")
        },
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'options', OptionViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'guest-votes', GuestVoteViewSet)
router.register(r'pollanalytics', PollAnalyticsViewSet)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('token/', TokenObtainPairViewPatched.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshViewPatched.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
