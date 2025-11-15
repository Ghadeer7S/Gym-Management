from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone
import string, random

class User(AbstractUser):
    ROLE_MEMBER = 'M'
    ROLE_ADMIN = 'A'
    ROLE_COACH = 'C'

    ROLE_CHOICES = [
        (ROLE_MEMBER, 'MEMBER'),
        (ROLE_ADMIN, 'ADMIN'),
        (ROLE_COACH, 'COACH')
    ]

    username = models.CharField(max_length=255, unique=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, null=True, blank=True)
    activation_expires_at = models.DateTimeField(null=True, blank=True)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    reset_expires_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # activation code
    def generate_activation_code(self):
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        self.activation_code = code
        self.activation_expires_at = timezone.now() + timedelta(minutes=5)
        self.save()

    def is_activation_code_valid(self, code):
        if (self.activation_code == code
            and self.activation_expires_at
            and timezone.now() < self.activation_expires_at
            ):  return True
        return False
    
    # reset code
    def generate_reset_code(self, minutes_valid=5):
        code = ''.join(\
            random.choices(string.digits + string.ascii_uppercase, k=6))
        self.reset_code = code
        self.reset_expires_at = timezone.now() + timedelta(minutes=minutes_valid)
        self.save(update_fields=['reset_code', 'reset_expires_at'])
        return code
    
    def is_reset_code_valid(self, code):
        if (self.reset_code == code
            and self.reset_expires_at
            and timezone.now() < self.reset_expires_at):
            return True
        return False
    
    def clear_reset_code(self):
        self.reset_code = None
        self.reset_expires_at = None
        self.save(update_fields=['reset_code', 'reset_expires_at'])

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
            self.is_approved = True
            self.is_active = True

        if self.role == self.ROLE_ADMIN:
            self.is_staff = True

        if self.role == self.ROLE_MEMBER:
            self.is_approved = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email