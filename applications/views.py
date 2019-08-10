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
def PostgradApplicationsDashboard(request):
    applications = Application.objects.filter(postgrad_profile=request.user.postgrad_profile)
    return render(request, 'postgrad_applications_dashboard.html', {'applications': applications})