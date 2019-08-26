from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from applications.forms import NewApplicationForm
from applications.models import Application
from postgrad.forms import CreateProfileForm
from postgrad.models import PostgradProfile


def postgrad_check(user):
    return user.is_postgrad


def new_postgrad_check(user):
    return not (user.is_staff and user.is_postgrad)


@login_required
@user_passes_test(new_postgrad_check)
def create_profile_view(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            profile = PostgradProfile(user=request.user, student_number=form.cleaned_data['student_number'],
                                      first_name=form.cleaned_data['first_name'],
                                      last_name=form.cleaned_data['last_name']
                                      )
            profile.user.is_postgrad = True
            profile.save()
            profile.user.save()
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        form = CreateProfileForm()
    return render(request, 'create_profile.html', {'form': form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_dashboard_view(request):
    return render(request, 'postgrad_dashboard.html', {"fname": request.user.postgrad_profile.first_name,
                                                       "lname": request.user.postgrad_profile.last_name})

@login_required
@user_passes_test(postgrad_check)
def postgrad_applications_dashboard_view(request):
    applications = Application.objects.filter(postgrad_profile=request.user.postgrad_profile)
    return render(request, 'postgrad_applications_dashboard.html', {'applications': applications})


@login_required
@user_passes_test(postgrad_check)
def postgrad_remove_application_view(request, id):
    application = Application.objects.filter(id=id)
    application.delete()
    return HttpResponseRedirect(reverse('postgrad_applications_dashboard'))
