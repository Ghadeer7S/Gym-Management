from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ValidationError

User = get_user_model()

def validate_activation_data(email, code):
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        raise ValidationError({"email": "User not found."})
    if user.is_active:
        raise ValidationError({"email": "Account is already active."})
    if not user.is_activation_code_valid(code):
        raise ValidationError({"activation_code": "Invalid or expired activation code."})
    return user

def validate_resend_activation(email: str):
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        raise ValidationError("User not found.")

    if user.is_active:
        raise ValidationError("Account is already active.")

    return user

def validate_user_email(email: str):
    try:
        return User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        raise ValidationError({"email": "No user with this email."})

def validate_new_password_strength(password: str):
    try:
        validate_password(password)
    except ValidationError as e:
        raise ValidationError(list(e.messages))
    return password

def validate_password_reset_data(email, code):
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        raise ValidationError({"email": "User not found."})
    
    if not user.is_reset_code_valid(code):
        raise ValidationError({"code": "Invalid or expired reset code."})
    
    return user
