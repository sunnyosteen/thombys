from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# This signal is triggered after a User object is saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Create the user profile
        UserProfile.objects.create(user=instance)
        print(f"New user created: {instance.username} ({instance.email})")  # Output message to terminal

# This signal ensures that the user profile is saved every time the User is saved (for non-superusers)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()
        print(f"User profile saved for {instance.username} ({instance.email})")  # Output message to terminal
