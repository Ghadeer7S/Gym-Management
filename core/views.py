from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serializers import (
    CustomActivationSerializer, ResendActivationCodeSerializer,
    CustomPasswordResetRequestSerializer, CustomPasswordResetConfirmSerializer
)

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
        serializer.save()
        return Response(
            {"detail": "A new activation code has been generated."},
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
