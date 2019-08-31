from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import *
from.forms import *

def postgrad_check(user):
    return user.is_postgrad


def new_postgrad_check(user):
    return not (user.is_staff and user.is_postgrad)


def select_country_view(request):
    if request.method == 'POST':
        form = QualificationCountryForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('postgrad_edit_qualification', args=[form.cleaned_data["country"]]))
    else:
        form = QualificationCountryForm()
    return render(request, "select_country.html", {"form": form})


def edit_qualification_view(request, country):
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            qualification = Qualification.objects.get_or_create(degree=form.cleaned_data["external_degree"], university=form.cleaned_data["university"],
                                          min_years=form.cleaned_data["min_years"], thesis=form.cleaned_data["thesis"])[0]
            qualification.save()
            request.user.postgrad_profile.qualification = qualification
            request.user.postgrad_profile.save()
            return HttpResponseRedirect(reverse('postgrad_qualification_dashboard'))
    else:
        if request.user.postgrad_profile.qualification:
            form = QualificationForm({"degree": request.user.postgrad_profile.qualification.degree, "university": request.user.postgrad_profile.qualification.university,
                                  "min_years": request.user.postgrad_profile.qualification.min_years, "thesis": request.user.postgrad_profile.qualification.thesis})
        else:
            form = QualificationForm()
        form.fields['external_degree'] = forms.ModelChoiceField(ExternalDegree.objects.filter(country=country))
    return render(request, "postgrad_edit_qualification.html", {"form": form})


def postgrad_qualification_dashboard(request):
    return render(request, "postgrad_qualification_dashboard.html")


@login_required
@user_passes_test(postgrad_check)
def new_application_view(request):
    if request.method == 'POST':
        form = NewApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = Application(postgrad_profile=request.user.postgrad_profile,
                                      degree=form.cleaned_data['degree'], pdf=request.FILES['pdf'])
            if request.user.postgrad_profile.qualification not in form.cleaned_data['degree'].accepted_qualifications.all():
                application.reject()
                application.update_reason("You did not meet the minimum qualification requirements.")
            application.save()
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        form = NewApplicationForm()

    return render(request, 'applications/application_form.html', {'form': form})


class ApplicationUpdate(UpdateView):
    model = Application
    fields = ['degree','pdf']
    success_url = reverse_lazy('postgrad_applications_dashboard')

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

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('create_profile')
    template_name = 'register.html'