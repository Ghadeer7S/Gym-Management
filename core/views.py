from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    CustomActivationSerializer, ResendActivationCodeSerializer,
    CustomPasswordResetRequestSerializer, CustomPasswordResetConfirmSerializer
)
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets

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
    
class ResendActivationViewSet(viewsets.ViewSet):
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

class PasswordResetRequestViewSet(viewsets.ViewSet):
    serializer_class = CustomPasswordResetRequestSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.generate_reset_code()

        # إرسال الإيميل هنا بدلاً من signal
        send_mail(
            "Password Reset Request",
            f"Hello {user.first_name or user.username},\n\n"
            f"Your password reset code is: {user.reset_code}\n\n"
            "This code will expire in 5 minutes.\n",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"detail": "Reset code sent to email."})


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
