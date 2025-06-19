from django.db import models
from django.contrib.auth.models import User

class RoomBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_bookings')
    room_type = models.CharField(max_length=100)  # e.g., Standard, Deluxe, Suite
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.room_type} ({self.check_in} to {self.check_out})"

    class Meta:
        verbose_name = "ROOM BOOKING"
        verbose_name_plural = "ROOM BOOKINGS"


class EventBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_bookings')
    event_type = models.CharField(max_length=100)  # e.g., Wedding, Meeting
    hall = models.CharField(max_length=100)  # e.g., Hall A, Hall B
    date = models.DateField()
    time_slot = models.CharField(max_length=100)  # e.g., Morning, Evening
    expected_guests = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.hall} ({self.date})"

    class Meta:
        verbose_name = "EVENT BOOKING"
        verbose_name_plural = "EVENT BOOKINGS"
