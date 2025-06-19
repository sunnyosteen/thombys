from django.contrib import admin
from .models import RoomBooking, EventBooking

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'check_in', 'check_out', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected bookings as confirmed"

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'hall', 'date', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} booking(s) marked as confirmed.")
    approve_booking.short_description = "Mark selected bookings as confirmed"
