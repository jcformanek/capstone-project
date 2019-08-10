# users/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('', PostgradDashboardView, name='postgrad_dashboard'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create_profile', CreateProfileView, name='create_profile')
]