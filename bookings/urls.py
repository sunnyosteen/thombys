from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('room_list', views.room_list, name='room_list'),
    path('checkout/<int:space_id>/', views.checkout, name='checkout'),  # ✅ use space_id
    # urls.py
    path('checkout/process/', views.process_booking, name='process_booking'),
    path('checkout/payment/', views.payment_page, name='payment_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
