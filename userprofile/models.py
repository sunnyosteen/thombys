# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import RegexValidator

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
#     # Add username field to UserProfile with alphanumeric characters only
#     username_regex = RegexValidator(
#         regex=r'^[a-zA-Z0-9]+$',  # Allow only letters and numbers
#         message="Username can only contain letters and numbers."
#     )
#     username = models.CharField(
#         max_length=30,
#         unique=True,  # Ensure the username is unique
#         validators=[username_regex],
#         blank=False
#     )
    
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)

#     phone_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,15}$',
#         message="Phone number must be entered in the format: '+123456789'. Up to 15 digits."
#     )
#     phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

#     address = models.TextField(blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     country = models.CharField(max_length=100, blank=True)
#     profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

#     verified = models.BooleanField(default=False)
#     email_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.get_full_name() or self.user.username

#     class Meta:
#         verbose_name = "USER PROFILE"
#         verbose_name_plural = "USER PROFILES"


from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+123456789'. Up to 15 digits."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "USER PROFILE"
        verbose_name_plural = "USER PROFILES"
