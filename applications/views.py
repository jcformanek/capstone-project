from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from.forms import *


@login_required
def NewApplicationView(request):
    if request.method == 'POST':
        form = NewApplicationForm(request.POST)
        if form.is_valid():
            application = Application(postgrad_profile=request.user.postgrad_profile, degree=form.cleaned_data['degree'])
            application.save()
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        form = NewApplicationForm()

    return render(request, 'new_application.html', {'form': form})

@login_required
def PostgradRemoveApplicationView(request, num):
    application_id = num
    application = Application.objects.get(id=application_id)
    application.delete()
    return HttpResponseRedirect(reverse('postgrad_applications_dashboard'))

@login_required
def StaffRemoveApplicationView(request, num):
    application_id = num
    application = Application.objects.get(id=application_id)
    application.delete()
    return HttpResponseRedirect(reverse('staff_applications_dashboard'))

@login_required
def StaffAcceptApplicationView(request, num):
    application_id = num
    application = Application.objects.get(id=application_id)
    application.accept()
    application.save()
    return HttpResponseRedirect(reverse('staff_applications_dashboard'))

@login_required
def StaffRejectApplicationView(request, num):
    application_id = num
    application = Application.objects.get(id=application_id)
    application.reject()
    application.save()
    return HttpResponseRedirect(reverse('staff_applications_dashboard'))

@login_required
def PostgradApplicationsDashboard(request):
    applications = Application.objects.filter(postgrad_profile=request.user.postgrad_profile)
    return render(request, 'postgrad_applications_dashboard.html', {'applications': applications})

@login_required
def StaffApplicationsDashboard(request):
    applications = Application.objects.all()
    return render(request, 'staff_applications_dashboard.html', {'applications': applications})