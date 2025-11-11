from rest_framework.routers import DefaultRouter
from .views import ActivationViewSet, ResendActivationViewSet, PasswordResetRequestViewSet, PasswordResetConfirmViewSet

router = DefaultRouter()
router.register('activate', ActivationViewSet, basename='activate')
router.register('resend-activation', ResendActivationViewSet, basename='resend-activation')

router.register('password-reset/request', PasswordResetRequestViewSet, basename='password-reset-request')
router.register('password-reset/confirm', PasswordResetConfirmViewSet, basename='password-reset-confirm')

urlpatterns = router.urls