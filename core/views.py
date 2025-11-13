from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serializers import (
    CustomActivationSerializer, ResendActivationCodeSerializer,
    CustomPasswordResetRequestSerializer, CustomPasswordResetConfirmSerializer
)
from django.core.mail import send_mail
from django.conf import settings

class ActivationViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CustomActivationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Account activated successfully."},
            status=status.HTTP_200_OK
        )
    
class ResendActivationViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ResendActivationCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    
        subject = "Your Activation Code"
        message = (
            f"Hello {user.first_name},\n\n"
            f"Here is your new activation code: {user.activation_code}\n"
            f"This code will expire in 5 minutes.\n\n"
            f"If you didn’t request this, you can ignore this email."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

        return Response(
            {"detail": "A new activation code has been sent to your email."},
            status=status.HTTP_200_OK
        )

class PasswordResetRequestViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CustomPasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "A password reset code has been sent."},
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CustomPasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Your password has been reset successfully."},
            status=status.HTTP_200_OK
        )
