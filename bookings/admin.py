from django.contrib import admin
from .models import Space, RoomBooking, HallBooking


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('space_number', 'name', 'space_type', 'price', 'available')  # changed from room_number
    list_filter = ('space_type', 'available')
    search_fields = ('name', 'space_number')  # changed from room_number


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'space', 'check_in', 'check_out', 'status')
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} room booking(s) marked as approved.")
    approve_booking.short_description = "Mark selected room bookings as approved"


@admin.register(HallBooking)
class HallBookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'event_name', 'space', 'hall_number_display',
        'hall_price_display', 'hall_available_display',
        'event_date', 'status'
    )
    list_filter = ('status',)
    actions = ['approve_booking']

    def approve_booking(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} hall booking(s) marked as approved.")
    approve_booking.short_description = "Mark selected hall bookings as approved"

    def hall_number_display(self, obj):
        return obj.space.space_number if obj.space else "N/A"  # changed from room_number
    hall_number_display.short_description = 'Space Number'

    def hall_price_display(self, obj):
        return obj.space.price if obj.space else "N/A"
    hall_price_display.short_description = 'Hall Price'

    def hall_available_display(self, obj):
        return obj.space.available if obj.space else "N/A"
    hall_available_display.short_description = 'Available'
