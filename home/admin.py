from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import Gallery 
from bookings.models import Space, RoomBooking, HallBooking
from userprofile.models import UserProfile

# Django built-in models
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


# Custom Admin Site
class MyAdminSite(AdminSite):
    site_header = 'Thombys Place Admin'
    site_title = 'Thombys Place Admin Portal'
    index_title = 'Welcome to Thombys Place Admin'


# Instantiate custom admin site
admin_site = MyAdminSite(name='myadmin')


# Gallery Admin
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    readonly_fields = ('created_at',)


# ✅ Fixed: Space Admin (Room and Hall)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('space_number', 'name', 'space_type', 'price', 'available')  # corrected from room_number
    list_filter = ('space_type', 'available')
    search_fields = ('name', 'space_number')  # corrected from room_number


# RoomBooking Admin
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'space', 'get_room_type', 'check_in', 'check_out', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def get_room_type(self, obj):
        return obj.space.get_space_type_display() if obj.space else "N/A"
    get_room_type.short_description = 'Room Type'

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} room booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected room bookings as confirmed"


# HallBooking Admin
class HallBookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'event_name', 'space', 'hall_number_display',
        'hall_price_display', 'hall_available_display',
        'event_date', 'status'
    )
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} hall booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected hall bookings as confirmed"

    def hall_number_display(self, obj):
        return obj.space.space_number if obj.space else "N/A"  # corrected from room_number
    hall_number_display.short_description = 'Space Number'

    def hall_price_display(self, obj):
        return obj.space.price if obj.space else "N/A"
    hall_price_display.short_description = 'Hall Price'

    def hall_available_display(self, obj):
        return obj.space.available if obj.space else "N/A"
    hall_available_display.short_description = 'Available'


# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'verified', 'email_verified', 'created_at')
    list_editable = ('phone', 'city', 'country', 'verified', 'email_verified')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('verified', 'email_verified')


# Register models to the custom admin site
admin_site.register(Gallery, GalleryAdmin)
admin_site.register(Space, SpaceAdmin)
admin_site.register(RoomBooking, RoomBookingAdmin)
admin_site.register(HallBooking, HallBookingAdmin)
admin_site.register(UserProfile, UserProfileAdmin)

# Register default auth models
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# ✅ Use the custom admin site
admin.site = admin_site
