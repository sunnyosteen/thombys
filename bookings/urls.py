from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('checkout/<int:space_id>/', views.checkout, name='checkout'),  # ✅ use space_id
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
