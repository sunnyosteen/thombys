# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  # URL for About page
    path('services/', views.services, name='services'),  # URL for About page
    path('contact/', views.contact, name='contact'),  # URL for About page
    # path('room/', views.room, name='room'),  # URL for Room View page
    # path('hall/', views.hall, name='hall'),  # URL for Hall View page
]
