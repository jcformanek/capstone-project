from django.urls import path
from .views import *


# urlpatterns = [
#     path('', application_redirect_view, name='application_redirect'),
#     path('new-application', NewApplicationView, name='new_application'),
#     path('my-applications', PostgradApplicationsDashboard, name='postgrad_applications_dashboard'),
#     path('remove<int:num>', StaffRemoveApplicationView, name='remove_application'),
#     path('premove<int:num>', PostgradRemoveApplicationView, name='postgrad_remove_application'),
#     path('accept<int:num>', StaffAcceptApplicationView, name='accept_application'),
#     path('reject<int:num>', StaffRejectApplicationView, name='reject_application'),
#     path('staff_dashboard', StaffApplicationsDashboard, name='staff_applications_dashboard')
# ]