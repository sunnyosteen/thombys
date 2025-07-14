from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property

class Space(models.Model):
    SPACE_TYPE_CHOICES = [
        ('room', 'Room'),
        ('hall', 'Hall'),
    ]

    space_number = models.CharField(max_length=10, unique=True)  # Renamed from room_number
    space_type = models.CharField(max_length=10, choices=SPACE_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='space_images/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_space_type_display()} - {'Available' if self.available else 'Unavailable'}"


class Booking(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('declined', 'Declined'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    booking_code = models.CharField(max_length=20, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-booked_at']


class RoomBooking(Booking):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_bookings')
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        limit_choices_to={'space_type': 'room'},
        related_name='room_bookings',
        null=True,
        blank=True
    )

    def __str__(self):
        space_name = self.space.name if self.space else "No Room"
        return f"{self.user.username} - Room: {space_name} ({self.status})"


class HallBooking(Booking):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hall_bookings')
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        limit_choices_to={'space_type': 'hall'},
        related_name='hall_bookings',
        null=True,
        blank=True
    )
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()

    def __str__(self):
        space_name = self.space.name if self.space else "No Hall"
        return f"{self.user.username} - {self.event_name} in {space_name} on {self.event_date} ({self.status})"

    @cached_property
    def hall_name(self):
        return self.space.name if self.space else None

    @cached_property
    def hall_price(self):
        return self.space.price if self.space else None

    @cached_property
    def hall_image(self):
        return self.space.image.url if self.space and self.space.image else None

    @cached_property
    def hall_number(self):
        return self.space.space_number if self.space else None  # Updated field name

    @cached_property
    def hall_availability(self):
        return self.space.available if self.space else None
