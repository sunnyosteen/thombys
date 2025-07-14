from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Space, RoomBooking, HallBooking
from .forms import BookingForm


@login_required
def room_list(request):
    rooms = Space.objects.filter(space_type='room', available=True)
    return render(request, 'bookings/room_list.html', {'rooms': rooms})


@login_required
def checkout(request, space_id):  # ✅ Updated to use space_id
    space = get_object_or_404(Space, id=space_id, space_type='room')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        amount = request.POST.get('calculated_amount') or space.price

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space
            booking.amount = amount
            booking.status = 'pending'
            booking.save()
            messages.success(request, "Booking submitted and is now pending approval.")
            return redirect('userprofile:dashboard')  # ✅ Redirect to user profile dashboard
    else:
        form = BookingForm()

    return render(request, 'bookings/checkout.html', {'space': space, 'form': form})


@login_required
def dashboard(request):
    room_bookings = RoomBooking.objects.filter(user=request.user)
    hall_bookings = HallBooking.objects.filter(user=request.user)
    return render(request, 'userprofile/dashboard.html', {
        'room_bookings': room_bookings,
        'hall_bookings': hall_bookings
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.warning(request, "Room booking cancelled.")
    return redirect('userprofile:dashboard')  # ✅ consistent redirection


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
    if booking.status in ['cancelled', 'declined']:
        booking.delete()
        messages.success(request, "Room booking deleted.")
    return redirect('userprofile:dashboard')
