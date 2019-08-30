from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('postgrad', postgrad_dashboard_view, name='postgrad_dashboard'),
    path('postgrad/create_profile', create_profile_view, name='create_profile'),
    path('postgrad/applications', postgrad_applications_dashboard_view, name='postgrad_applications_dashboard'),
    path('postgrad/qualifications', edit_qualification_view, name='postgrad_edit_qualification'),
    path('postgrad/applications/remove/<int:id>', postgrad_remove_application_view, name='postgrad_remove_application'),
    path('postgrad/new-application', new_application_view, name='new_application'),
    path('postgrad/application/<int:pk>/update/', ApplicationUpdate.as_view(), name='application_update'),
    path('staff', staff_dashboard_view, name='staff_dashboard'),
    path('staff/applications', staff__applications_dashboard_view, name='staff_applications_dashboard'),
    path('staff/applications/<int:id>/', staff__application_detailed_view, name='staff_application_detailed'),
    path('staff/applications/accept/<int:id>/', staff_accept_application_view, name='staff_accept_application'),
    path('staff/applications/reject/<int:id>/', staff_reject_application_view, name='staff_reject_application')
]