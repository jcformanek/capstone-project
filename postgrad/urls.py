from django.urls import path, include

from applications.views import *
from .views import *


urlpatterns = [
    path('', postgrad_dashboard_view, name='postgrad_dashboard'),
    path('create_profile', create_profile_view, name='create_profile'),
    path('applications', postgrad_applications_dashboard_view, name='postgrad_applications_dashboard'),
    path('applications/remove/<int:id>', postgrad_remove_application_view, name='postgrad_remove_application'),
    path('new-application', new_application_view, name='new_application')
]