from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import Gallery 
from bookings.models import RoomBooking, EventBooking
from userprofile.models import UserProfile

# Django built-in models
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


# Create a custom admin site
class MyAdminSite(AdminSite):
    site_header = 'Thombys Place Admin'
    site_title = 'Thombys Place Admin Portal'
    index_title = 'Welcome to Thombys Place Admin'


# Instantiate the custom admin site
admin_site = MyAdminSite(name='myadmin')


# Admin class for Gallery
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    readonly_fields = ('created_at',)


# Admin class for RoomBooking
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'check_in', 'check_out', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected bookings as confirmed"


# Admin class for EventBooking
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'hall', 'date', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected bookings as confirmed"


# Admin class for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'verified', 'email_verified', 'created_at')
    list_editable = ('phone', 'city', 'country', 'verified', 'email_verified')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('verified', 'email_verified')


# Register all models to the custom admin site
admin_site.register(Gallery, GalleryAdmin)
admin_site.register(RoomBooking, RoomBookingAdmin)
admin_site.register(EventBooking, EventBookingAdmin)
admin_site.register(UserProfile, UserProfileAdmin)

# Register Django's built-in auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Optional: Override the default admin site (do this only if you're replacing the default admin entirely)
admin.site = admin_site
