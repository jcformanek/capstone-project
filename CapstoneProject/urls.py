# djauth/postgrad_urls.py
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', dashboard_redirect_view, name='home'),
    path('admin/', admin.site.urls),
    path('applications/', include('applications.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]