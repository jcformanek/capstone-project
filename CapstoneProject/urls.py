# djauth/postgrad_urls.py
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', dashboard_redirect_view, name='home'),
    path('admin/', admin.site.urls),
    path('postgrad/', include('postgrad.urls')),
    path('staff/', include('staff.urls')),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]