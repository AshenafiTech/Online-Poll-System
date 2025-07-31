
from rest_framework.routers import DefaultRouter
from polls.api.viewsets import PollViewSet, ChoiceViewSet, VoteViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'choices', ChoiceViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = router.urls

# JWT Auth endpoints
from django.urls import path, re_path
from polls.api.user_views import UserRegistrationView
from polls.api.user_profile import UserProfileView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Online Poll System API",
        default_version='v1',
        description="API documentation for the Online Poll System",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('polls/<int:pk>/vote/', PollViewSet.as_view({'post': 'vote'}), name='poll-vote'),
    path('polls/<int:pk>/results/', PollViewSet.as_view({'get': 'results'}), name='poll-results'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
