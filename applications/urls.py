from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('postgrad', postgrad_dashboard_view, name='postgrad_dashboard'),
    path('postgrad/create_profile/<str:inter>', create_profile_view, name='postgrad_create_profile'),
    path('postgrad/edit_profile/', postgrad_edit_details_view, name='postgrad_edit_profile'),
    path('postgrad/select_citizenship/', postgrad_citizenship_select_view, name='postgrad_select_citizenship'),
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
    path('postgrad/application/view/<int:app_id>', postgrad_application_view, name='postgrad_view_application'),
    path('staff', staff_dashboard_view, name='staff_dashboard'),
    path('staff/applications/filter-by-degree/', staff_select_uct_degree_filter_view, name='staff_select_uct_degree_filter'),
    path('staff/applications/filter-by-accepted/', staff_filter_by_accepted_view, name='staff_filter_by_accepted'),
    path('staff/applications/filter-by-rejected/', staff_filter_by_rejected_view, name='staff_filter_by_rejected'),
    path('staff/applications/filter-by-degree/<int:degree_id>', staff_filter_by_degree_view, name='staff_filter_by_degree'),
    path('staff/application/<int:app_id>/', staff_view_application, name='staff_view_application'),
    path('staff/applications/accept/<int:id>/', staff_accept_application_view, name='staff_accept_application'),
    path('staff/applications/reject/<int:id>/', staff_reject_application_view, name='staff_reject_application'),
    path('staff/application/as_pdf/<int:id>/', staff_application_as_pdf, name='staff_application_as_pdf'),
    path('staff/application/add_reason/<int:id>/', staff_add_reason, name='staff_add_reason'),
    path('staff/application/lock/<int:id>/', staff_lock, name='staff_lock'),
    path('staff/application/unlock/<int:id>/', staff_unlock, name='staff_unlock'),
    path('staff/applications/as_csv/<int:id>/', staff_applications_filtered_by_degree_as_csv, name='staff_applications_filtered_by_degree_as_csv'),
    path('staff/applications/as_csv/accepted/', staff_filtered_by_accepted_as_csv, name='staff_filtered_by_accepted_as_csv'),
    path('staff/applications/as_csv/rejected/', staff_filtered_by_rejected_as_csv, name='staff_filtered_by_rejected_as_csv')
]