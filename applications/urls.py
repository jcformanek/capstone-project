from django.urls import path
from .views import *


urlpatterns = [
    path('new', NewApplicationView, name='new_application'),
    path('postgrad_dashboard', PostgradApplicationsDashboard, name='postgrad_applications_dashboard'),
]