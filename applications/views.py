from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import default_storage
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


def select_country_view(request, app_id):
    if request.method == 'POST':
        form = QualificationCountryForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('postgrad_update_qualification', args=[app_id, form.cleaned_data['country']]))
    else:
        form = QualificationCountryForm()
    return render(request, "select_country.html", {"form": form})


def edit_qualification_view(request, app_id, country):
    application = Application.objects.get(id=app_id)
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            qualification = Qualification.objects.get_or_create(degree=form.cleaned_data["external_degree"], university=form.cleaned_data["university"],
                                          min_years=form.cleaned_data["min_years"], thesis=form.cleaned_data["thesis"])[0]
            qualification.save()
            application.qualification = qualification
            application.save()
            return HttpResponseRedirect(reverse('postgrad_upload_pdf', args=[app_id]))
    else:
        if application.qualification:
            form = QualificationForm({"degree": application.qualification.degree, "university": application.qualification.university,
                                      "min_years": application.qualification.min_years, "thesis": application.qualification.thesis})
        else:
            form = QualificationForm()
        form.fields['external_degree'] = forms.ModelChoiceField(ExternalDegree.objects.filter(country=country))
    return render(request, "postgrad_edit_qualification.html", {"form": form})


def postgrad_application_view(request, app_id):
    application = Application.objects.get(id=app_id)
    return render(request, "postgrad_view_application.html", {"application": application})

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


def postgrad_upload_pdf_view(request, app_id):
    application = Application.objects.get(id=app_id)
    if request.method == 'POST' and request.FILES['pdf']:
        file = request.FILES['pdf']
        application.pdf = file
        application.save()
        return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        if application.pdf:
            form = UploadPdfForm({"pdf": application.pdf})
        else:
            form = UploadPdfForm()
    return render(request, "postgrad_pdf_upload.html", {"form": form})


def postgrad_new_select_uct_degree_view(request):
    if request.method == 'POST':
        form = SelectUCTDegree(request.POST)
        if form.is_valid():
            app = Application.objects.get_or_create(postgrad_profile=request.user.postgrad_profile,
                                                    degree=form.cleaned_data['degree'])[0]
            app.save()
            return HttpResponseRedirect(reverse('postgrad_update_application', args=[app.id]))
    else:
        form = SelectUCTDegree()
    return render(request, "postgrad_select_uct_degree.html", {"form": form})


def postgrad_edit_select_uct_degree_view(request, app_id):
    app = Application.objects.get(id=app_id)
    if request.method == 'POST':
        form = SelectUCTDegree(request.POST)
        if form.is_valid():
            app.degree = form.cleaned_data["degree"]
            app.save()
            return HttpResponseRedirect(reverse('postgrad_select_country', args=[app.id]))
    else:
        form = SelectUCTDegree({"degree": app.degree})
    return render(request, "postgrad_select_uct_degree.html", {"form": form})


class ApplicationUpdate(UpdateView):
    model = Application
    fields = ['degree', 'pdf']
    success_url = reverse_lazy('postgrad_applications_dashboard')


def postgrad_new_application_part1(request):
    if request.method == "POST":
        form = NewApplicationForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data["country"]
            degree = form.cleaned_data["degree"]
            return HttpResponseRedirect(reverse('postgrad_new_application_part2', args=[degree.id, country]))
    else:
        form = NewApplicationForm()
    return render(request, "new_application_part1.html", {"form": form})


def postgrad_new_application_part2(request, degree_id, country):
    degree = UCTDegree.objects.get(id=degree_id)
    if request.method == 'POST':
        form = QualificationForm(country, request.POST)
        if form.is_valid():
            application = Application(degree=degree, postgrad_profile=request.user.postgrad_profile)
            application.qualification = form.save()
            application.save()
            return HttpResponseRedirect(reverse('postgrad_update_application', args=[application.id]))
    else:
        form = QualificationForm(country=country)
    return render(request, "applications/qualification_form.html", {"form": form})


def postgrad_update_application(request, app_id):
    application = Application.objects.get(id=app_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('postgrad_view_application', args=[app_id]))
    else:
        form = ApplicationForm(instance=application)
    return render(request, "applications/application_form.html", {"form": form})


def postgrad_update_qualification(request, app_id, country):
    application = Application.objects.get(id=app_id)
    qualification = application.qualification
    if request.method == 'POST':
        form = QualificationForm(country, request.POST)
        if form.is_valid():
            qualification = form.save()
            application.qualification = qualification
            application.save()
            return HttpResponseRedirect(reverse('postgrad_view_application', args=[app_id]))
    else:
        form = QualificationForm(instance=qualification, country=country)
    return render(request, "applications/qualification_form.html", {"form": form})

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
    applications = Application.objects.filter(postgrad_profile=request.user.postgrad_profile)
    return render(request, 'postgrad_dashboard.html', {"fname": request.user.postgrad_profile.first_name,
                                                       "lname": request.user.postgrad_profile.last_name,
                                                       "applications": applications})


@login_required
@user_passes_test(postgrad_check)
def postgrad_remove_application_view(request, id):
    application = Application.objects.filter(id=id)
    application.delete()
    return HttpResponseRedirect(reverse('postgrad_dashboard'))

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