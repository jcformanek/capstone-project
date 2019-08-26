from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from applications.models import Application


def staff_check(user):
    return user.is_staff


@login_required
@user_passes_test(staff_check)
def staff_dashboard_view(request):
    return render(request, 'staff_dashboard.html', {"fname": request.user.staff_profile.first_name,
                                                       "lname": request.user.staff_profile.last_name})


@login_required
@user_passes_test(staff_check)
def staff__applications_dashboard_view(request):
    applications = Application.objects.all()
    return render(request, 'staff_applications_dashboard.html', {'applications': applications})


@login_required
@user_passes_test(staff_check)
def staff__application_detailed_view(request, id):
    application = Application.objects.get(id=id)
    return render(request, 'staff_application_detailed.html', {'application': application})


@login_required
@user_passes_test(staff_check)
def staff_accept_application_view(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.accept()
    application.save()
    return HttpResponseRedirect(reverse('staff_applications_dashboard'))


@login_required
@user_passes_test(staff_check)
def staff_reject_application_view(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.reject()
    application.save()
    return HttpResponseRedirect(reverse('staff_applications_dashboard'))
