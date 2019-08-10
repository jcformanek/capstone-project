# users/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.db import models
from .models import *

from .forms import CustomUserCreationForm, CreateProfileForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('create_profile')
    template_name = 'signup.html'


@login_required
def CreateProfileView(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            profile = PostgradProfile(user=request.user, student_number=form.cleaned_data['student_number'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            profile.save()
            return HttpResponseRedirect(reverse('postgrad_dashboard'))

    # if a GET (or any other method) we'll create a blank form
    else:
        if hasattr(request.user, "postgrad_profile"):
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
        else:
            form = CreateProfileForm()

    return render(request, 'create_profile.html', {'form': form})

@login_required
def PostgradDashboardView(request):
    firstname = request.user.postgrad_profile.first_name
    lastname = request.user.postgrad_profile.last_name
    return render(request, 'postgrad_dashboard.html', {"fname": firstname, "lname":lastname})

