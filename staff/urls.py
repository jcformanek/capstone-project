from django.urls import path
from .views import *


urlpatterns = [
    path('', staff_dashboard_view, name='staff_dashboard'),
    path('applications', staff__applications_dashboard_view, name='staff_applications_dashboard'),
    path('applications/<int:id>/', staff__application_detailed_view, name='staff_application_detailed'),
    path('applications/accept/<int:id>/', staff_accept_application_view, name='staff_accept_application'),
    path('applications/reject/<int:id>/', staff_reject_application_view, name='staff_reject_application')
]