from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance)
        print(f"✅ New user profile created for: {instance.username} ({instance.email})")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        try:
            instance.userprofile.save()
            print(f"💾 UserProfile saved for: {instance.username} ({instance.email})")
        except UserProfile.DoesNotExist:
            print(f"❌ UserProfile does not exist for: {instance.username} — skipping save.")
