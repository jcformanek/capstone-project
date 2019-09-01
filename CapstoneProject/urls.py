# djauth/postgrad_urls.py
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from CapstoneProject import settings
from .views import *

urlpatterns = [
    path('', dashboard_redirect_view, name='home'),
    path('admin/', admin.site.urls),
    path('applications/', include('applications.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)