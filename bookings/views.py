from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Space, RoomBooking, HallBooking
from .forms import BookingForm

@login_required
def room_list(request):
    rooms = Space.objects.filter(space_type='room', available=True)
    halls = Space.objects.filter(space_type='hall', available=True)
    return render(request, 'bookings/room_list.html', {'rooms': rooms, 'halls': halls})


@login_required
def checkout(request, space_id):
    space = get_object_or_404(Space, id=space_id)

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
            return redirect('userprofile:dashboard')
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
    return redirect('userprofile:dashboard')


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
    if booking.status in ['cancelled', 'declined']:
        booking.delete()
        messages.success(request, "Room booking deleted.")
    return redirect('userprofile:dashboard')


@login_required
def process_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            space_id = request.POST.get('space_id')
            booking.space = get_object_or_404(Space, id=space_id)
            booking.amount = request.POST.get('calculated_amount')
            booking.status = 'pending'  # ✅ fixed casing
            booking.save()
            request.session['booking_id'] = booking.id
            return redirect('bookings:payment_page')
    return redirect('bookings:room_list')



# ✅ Use RoomBooking to fetch the booking
@login_required
def payment_page(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('bookings:room_list')
    booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
    return render(request, 'bookings/payment.html', {'booking': booking})
