from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions, serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .validators import (
    validate_activation_data, validate_resend_activation,
    validate_user_email, validate_new_password_strength,
    validate_password_reset_data
)
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                   'email', 'first_name', 'last_name', 'role', 'is_approved']
        read_only_fields = ['is_approved']
    
    def create(self, validated_data):
        user = super().create(validated_data)

        # Generate activation code before the signal fires
        user.generate_activation_code()

        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_approved:
            raise exceptions.AuthenticationFailed(
                detail="Your account is pending admin approval. You cannot log in yet.",
                code="user_not_approved"
            )
        data['role'] = self.user.role
        return data
    
class CustomActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user = validate_activation_data(attrs.get("email"), attrs.get("activation_code"))
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.is_active = True
        user.activation_code = None
        user.activation_expires_at = None
        user.save()
        return user
    
class ResendActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        user = validate_resend_activation(attrs.get("email"))
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        code = user.generate_activation_code()
        return user

class CustomPasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, attrs):
        user = validate_user_email(attrs.get("email"))
        attrs["user"] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.generate_reset_code()
        return user

class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        return validate_new_password_strength(value)
    
    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        user = validate_password_reset_data(email, code)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]

        user.set_password(new_password)
        user.clear_reset_code()
        user.save(update_fields=["password"])

        return user
