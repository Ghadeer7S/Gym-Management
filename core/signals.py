from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from djoser.signals import user_registered
from .models import User

@receiver(user_registered)
def send_welcome_email_after_registration(sender, user, request, **kwargs):
    subject = "Welcome to my Gym 💪"
    message = (
            f"Hello {user.first_name}!\n\n"
            f"Thank you for registering at our app 🎉\n\n"
            f"Your activation code is: {user.activation_code}\n"
            f"This code will expire in 5 minutes.\n\n"
            f"We're happy to have you onboard!"
    )

    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False
    )