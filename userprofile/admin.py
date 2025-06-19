from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'username', 'phone', 'address', 'city', 'country',
        'profile_picture', 'verified', 'email_verified', 'created_at',
    )

    list_filter = ('verified', 'email_verified')
    search_fields = ('user__username', 'first_name', 'last_name', 'user__email', 'phone', 'city', 'country')
    ordering = ('-created_at',)

    # Explicitly move first_name, last_name, and username to the top of the form
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'user', 'username',  # Add username here
                'phone', 'address', 'city', 'country',
                'profile_picture', 'verified', 'email_verified',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    readonly_fields = ('created_at',)

    # Prepopulate first_name, last_name, and username from related User model
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # Prepopulate first_name, last_name, and username fields from related User model
            form.base_fields['first_name'].initial = obj.user.first_name
            form.base_fields['last_name'].initial = obj.user.last_name
            form.base_fields['username'].initial = obj.user.username  # Prepopulate username field
        return form

    def save_model(self, request, obj, form, change):
        # Ensure that first_name, last_name, and username are updated on the related User model
        obj.user.first_name = form.cleaned_data['first_name']
        obj.user.last_name = form.cleaned_data['last_name']
        obj.user.username = form.cleaned_data['username']  # Save username changes to the User model
        obj.user.save()  # Save changes to the User model
        super().save_model(request, obj, form, change)
