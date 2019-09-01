from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('postgrad', postgrad_dashboard_view, name='postgrad_dashboard'),
    path('postgrad/create_profile', create_profile_view, name='create_profile'),
    path('postgrad/application/update/<int:app_id>', postgrad_update_application, name='postgrad_update_application'),
    path('postgrad/application/qualification/select_country/<int:app_id>', select_country_view, name='postgrad_select_country'),
    path('postgrad/application/qualification/update/<int:app_id>/<str:country>', postgrad_update_qualification, name='postgrad_update_qualification'),
    path('postgrad/application/new-application/part1', postgrad_new_application_part1, name='postgrad_new_application_part1'),
    path('postgrad/application/new-application/part2/<int:degree_id>/<str:country>', postgrad_new_application_part2, name='postgrad_new_application_part2'),
    path('postgrad/application/select-degree/<int:app_id>', postgrad_edit_select_uct_degree_view, name='postgrad_edit_select_uct_degree'),
    path('postgrad/application/upload/<int:app_id>', postgrad_upload_pdf_view, name="postgrad_upload_pdf"),
    path('postgrad/application/qualification/select_country/<int:app_id>', select_country_view, name='postgrad_select_country'),
    path('postgrad/application/qualification/edit/<int:app_id>/<str:country>', edit_qualification_view, name='postgrad_edit_qualification'),
    path('postgrad/applications/remove/<int:id>', postgrad_remove_application_view, name='postgrad_remove_application'),
    # path('postgrad/new-application', new_application_view, name='new_application'),
    path('postgrad/application/view/<int:app_id>', postgrad_application_view, name='postgrad_view_application'),
    path('staff', staff_dashboard_view, name='staff_dashboard'),
    path('staff/applications', staff__applications_dashboard_view, name='staff_applications_dashboard'),
    path('staff/applications/<int:id>/', staff__application_detailed_view, name='staff_application_detailed'),
    path('staff/applications/accept/<int:id>/', staff_accept_application_view, name='staff_accept_application'),
    path('staff/applications/reject/<int:id>/', staff_reject_application_view, name='staff_reject_application')
]