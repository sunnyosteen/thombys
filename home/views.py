# home/views.py
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from .models import Gallery



def home(request):
    gallery_items = Gallery.objects.all().order_by('-created_at')
    return render(request, 'home/index.html', {'gallery_items': gallery_items})


# Function-based view to render the About page
def about(request):
    return render(request, 'home/about.html')




# Function-based view to render the About page
def services(request):
    return render(request, 'home/services.html')





# Function-based view to render the About page
def contact(request):
    return render(request, 'home/contact.html')




# Function-based view to render the About page
def room(request):
    return render(request, 'home/room.html')




# Function-based view to render the About page
def hall(request):
    return render(request, 'home/hall.html')




# def gallery_view(request):
#     gallery_items = Gallery.objects.all().order_by('-created_at')
#     return render(request, 'gallery.html', {'gallery_items': gallery_items})
