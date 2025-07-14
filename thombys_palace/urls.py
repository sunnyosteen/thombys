from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('bookings/', include('bookings.urls', namespace='bookings')),  # Include bookings app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
