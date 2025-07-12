# rewear_project/urls.py

from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add this line to include all of Django's built-in auth URLs
    # This will create URLs like /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Keep this line to include all of your app's URLs
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)