# userprofile/urls.py
from django.urls import path
from . import views



app_name = 'userprofile'  # Set the namespace for the app

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
]
