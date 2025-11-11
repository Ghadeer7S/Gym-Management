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

@receiver(post_save, sender=User)
def rsend_activation_email(sender, instance, created, **kwargs):
    if instance.activation_code and not instance.is_active:
        subject = "Your Activation Code"
        message = (
                f"Hello {instance.first_name},\n\n"
                f"Here is your new activation code: {instance.activation_code}\n"
                f"This code will expire in 5 minutes.\n\n"
                f"If you didn’t request this, you can ignore this email."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=True,
        )

@receiver(post_save, sender=User)
def send_password_reset_email(sender, instance, created, **kwargs):
    if instance.reset_code and not created:
        subject = "Password Reset Request"
        message = (
            f"Hello {instance.first_name or instance.username},\n\n"
            f"Your password reset code is: {instance.reset_code}\n\n"
            "This code will expire in 5 minutes.\n"
            "If you did not request a password reset, please ignore this message."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)