from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
import io
from django.http import FileResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate
import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from .models import *
from .forms import *


def postgrad_check(user):
    return user.is_postgrad


def staff_check(user):
    return user.is_staff


def new_postgrad_check(user):
    return not (user.is_staff and user.is_postgrad)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('postgrad_select_citizenship')
    template_name = 'register.html'


@login_required
@user_passes_test(new_postgrad_check)
def postgrad_citizenship_select_view(request):
    if request.method == 'POST':
        form = SelectCitizenshipForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('postgrad_create_profile', args=[form.cleaned_data["citizenship"]]))
    else:
        form = SelectCitizenshipForm()
    return render(request, 'postgrad_select_citizenship.html', {'form': form})


@login_required
@user_passes_test(new_postgrad_check)
def create_profile_view(request, inter):
    if request.method == 'POST':
        if inter == "International":
            form = CreateInterPostgradProfileForm(request.POST)
        else:
            form = CreateRSAPostgradProfileForm(request.POST)
        if form.is_valid():
            profile = form.save()
            profile.citizenship = inter
            profile.email = request.user.email
            profile.user = request.user
            profile.user.is_postgrad = True
            profile.save()
            profile.user.save()
            send_email("You registred for the CS application portal!",
                       "Hello, you used this email to sign up on the CS website! Thanks for signing up " +
                       profile.first_name + " " + profile.last_name, profile.email)
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        if inter == "International":
            form = CreateInterPostgradProfileForm()
        else:
            form = CreateRSAPostgradProfileForm()
    return render(request, 'create_profile.html', {'form': form})


@login_required
@user_passes_test(postgrad_check)
def select_country_view(request, app_id):
    if request.method == 'POST':
        form = QualificationCountryForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(
                reverse('postgrad_update_qualification', args=[app_id, form.cleaned_data['country']]))
    else:
        form = QualificationCountryForm()
    return render(request, "select_country.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def edit_qualification_view(request, app_id, country):
    application = Application.objects.get(id=app_id)
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            qualification = Qualification.objects.get_or_create(degree=form.cleaned_data["external_degree"],
                                                                university=form.cleaned_data["university"],
                                                                min_years=form.cleaned_data["min_years"],
                                                                thesis=form.cleaned_data["thesis"])[0]
            qualification.save()
            application.qualification = qualification
            application.save()
            return HttpResponseRedirect(reverse('postgrad_upload_pdf', args=[app_id]))
    else:
        if application.qualification:
            form = QualificationForm(
                {"degree": application.qualification.degree, "university": application.qualification.university,
                 "min_years": application.qualification.min_years, "thesis": application.qualification.thesis})
        else:
            form = QualificationForm()
        form.fields['external_degree'] = forms.ModelChoiceField(ExternalDegree.objects.filter(country=country))
    return render(request, "postgrad_edit_qualification.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_application_view(request, app_id):
    application = Application.objects.get(id=app_id)
    return render(request, "postgrad_view_application.html", {"application": application})


@login_required
@user_passes_test(postgrad_check)
def new_application_view(request):
    if request.method == 'POST':
        form = NewApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = Application(postgrad_profile=request.user.postgrad_profile,
                                      degree=form.cleaned_data['degree'], pdf=request.FILES['pdf'])
            if request.user.postgrad_profile.qualification not in form.cleaned_data[
                'degree'].accepted_qualifications.all():
                application.reject()
                application.update_reason("You did not meet the minimum qualification requirements.")
            application.save()
            return HttpResponseRedirect(reverse('postgrad_dashboard'))
    else:
        form = NewApplicationForm()

    return render(request, 'applications/application_form.html', {'form': form})


@login_required
@user_passes_test(postgrad_check)
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


@login_required
@user_passes_test(postgrad_check)
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


@login_required
@user_passes_test(postgrad_check)
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


@login_required
@user_passes_test(postgrad_check)
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


@login_required
@user_passes_test(postgrad_check)
def postgrad_new_application_part2(request, degree_id, country):
    degree = UCTDegree.objects.get(id=degree_id)
    if request.method == 'POST':
        form = QualificationForm(country, request.POST)
        if form.is_valid():
            application = Application(degree=degree, postgrad_profile=request.user.postgrad_profile)
            application.qualification = form.save()
            application.save()
            application.check_qualifications()
            return HttpResponseRedirect(reverse('postgrad_update_application', args=[application.id]))
    else:
        form = QualificationForm(country=country)
    return render(request, "applications/qualification_form.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_update_application(request, app_id):
    application = Application.objects.get(id=app_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            app = form.save()
            app.check_qualifications()
            return HttpResponseRedirect(reverse('postgrad_view_application', args=[app_id]))
    else:
        form = ApplicationForm(instance=application)
    return render(request, "applications/application_form.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_update_qualification(request, app_id, country):
    application = Application.objects.get(id=app_id)
    qualification = application.qualification
    if request.method == 'POST':
        form = QualificationForm(country, request.POST)
        if form.is_valid():
            qualification = form.save()
            application.qualification = qualification
            application.save()
            application.check_qualifications()
            return HttpResponseRedirect(reverse('postgrad_view_application', args=[app_id]))
    else:
        form = QualificationForm(instance=qualification, country=country)
    return render(request, "applications/qualification_form.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_dashboard_view(request):
    applications = Application.objects.filter(postgrad_profile=request.user.postgrad_profile)
    return render(request, 'postgrad_dashboard.html', {"fname": request.user.postgrad_profile.first_name,
                                                       "lname": request.user.postgrad_profile.last_name,
                                                       "applications": applications})


@login_required
@user_passes_test(postgrad_check)
def postgrad_edit_details_view(request):
    postgrad = request.user.postgrad_profile
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=postgrad)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("postgrad_dashboard"))
    else:
        form = EditProfileForm(instance=postgrad)
    return render(request, "postgrad_edit_details.html", {"form": form})


@login_required
@user_passes_test(postgrad_check)
def postgrad_remove_application_view(request, id):
    application = Application.objects.filter(id=id)
    application.delete()
    return HttpResponseRedirect(reverse('postgrad_dashboard'))


@login_required
@user_passes_test(staff_check)
def staff_dashboard_view(request):
    applications = Application.objects.all()
    return render(request, 'staff_dashboard.html', {"fname": request.user.staff_profile.first_name,
                                                    "lname": request.user.staff_profile.last_name,
                                                    'applications': applications})


@login_required
@user_passes_test(staff_check)
def staff_view_application(request, app_id):
    application = Application.objects.get(id=app_id)
    return render(request, 'staff_view_application.html', {'application': application})


@login_required
@user_passes_test(staff_check)
def staff_accept_application_view(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.accept()
    application.add_evaluator(request.user.staff_profile)
    application.save()
    return HttpResponseRedirect(reverse('staff_add_reason', args=[id]))


@login_required
@user_passes_test(staff_check)
def staff_add_reason(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    if request.method == "POST":
        form = ReasonForm(request.POST)
        if form.is_valid():
            application.add_reason(form.cleaned_data["reason"])
            application.save()
            send_email("Application status change!", "Your application status was changed to " +
                       application.status + "! Reason: " + application.reason, application.postgrad_profile.email)
            return HttpResponseRedirect(reverse('staff_view_application', args=[id]))
    else:
        form = ReasonForm()
    return render(request, 'staff_reason.html', {"form": form})


@login_required
@user_passes_test(staff_check)
def staff_reject_application_view(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.reject()
    application.add_evaluator(request.user.staff_profile)
    application.save()
    return HttpResponseRedirect(reverse('staff_add_reason', args=[id]))


@login_required
@user_passes_test(staff_check)
def staff_select_uct_degree_filter_view(request):
    if request.method == "POST":
        form = SelectUCTDegree(request.POST)
        if form.is_valid():
            degree = form.cleaned_data["degree"]
            return HttpResponseRedirect(reverse("staff_filter_by_degree", args=[degree.id]))
    else:
        form = SelectUCTDegree()
    return render(request, "staff_select_degree.html", {"form": form})


@login_required
@user_passes_test(staff_check)
def staff_filter_by_degree_view(request, degree_id):
    degree = UCTDegree.objects.get(id=degree_id)
    applications = Application.objects.filter(degree=degree)
    return render(request, "staff_filter_by_degree.html", {"applications": applications, "degree": degree})


@login_required
@user_passes_test(staff_check)
def staff_filter_by_accepted_view(request):
    applications = Application.objects.filter(is_accepted=True)
    return render(request, "staff_filter_by_accepted.html", {"applications": applications})


@login_required
@user_passes_test(staff_check)
def staff_filter_by_rejected_view(request):
    applications = Application.objects.filter(is_rejected=True)
    return render(request, "staff_filter_by_rejected.html", {"applications": applications})


@login_required
@user_passes_test(staff_check)
def staff_application_as_pdf(request, id):
    application = Application.objects.get(id=id)
    buffer = io.BytesIO()
    my_doc = SimpleDocTemplate(buffer)
    flowables = []
    sample_style_sheet = getSampleStyleSheet()
    paragraph_1 = Paragraph("Application", sample_style_sheet['Heading1'])
    paragraph_2 = Paragraph("Student number: " + application.postgrad_profile.student_number,
                            sample_style_sheet['BodyText'])
    paragraph_3 = Paragraph("Applying for: " + application.degree.name, sample_style_sheet['BodyText'])
    paragraph_4 = Paragraph("Previous Degree: " + str(application.qualification.degree), sample_style_sheet['BodyText'])
    paragraph_5 = Paragraph("Minimum years of previous degree: " + str(application.qualification.min_years),
                            sample_style_sheet['BodyText'])
    paragraph_6 = Paragraph("Thesis complete: " + str(application.qualification.thesis), sample_style_sheet['BodyText'])
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    flowables.append(paragraph_3)
    flowables.append(paragraph_4)
    flowables.append(paragraph_5)
    flowables.append(paragraph_6)
    my_doc.build(flowables)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='application.pdf')


@login_required
@user_passes_test(staff_check)
def staff_applications_filtered_by_degree_as_csv(request, id):
    degree = UCTDegree.objects.get(id=id)
    applications = Application.objects.filter(degree=degree)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    writer = csv.writer(response)
    writer.writerow(["degree", 'student number', 'status'])
    for app in applications:
        writer.writerow([degree, app.postgrad_profile.student_number, app.status])
    return response


@login_required
@user_passes_test(staff_check)
def staff_filtered_by_accepted_as_csv(request):
    applications = Application.objects.filter(is_accepted=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    writer = csv.writer(response)
    writer.writerow(["degree", 'student number', 'status'])
    for app in applications:
        writer.writerow([app.degree, app.postgrad_profile.student_number, app.status])
    return response


@login_required
@user_passes_test(staff_check)
def staff_filtered_by_rejected_as_csv(request):
    applications = Application.objects.filter(is_accepted=False)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    writer = csv.writer(response)
    writer.writerow(["degree", 'student number', 'status'])
    for app in applications:
        writer.writerow([app.degree, app.postgrad_profile.student_number, app.status])
    return response


@login_required
@user_passes_test(staff_check)
def staff_lock(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.lock()
    application.save()
    return HttpResponseRedirect(reverse('staff_view_application', args=[id]))


@login_required
@user_passes_test(staff_check)
def staff_unlock(request, id):
    application_id = id
    application = Application.objects.get(id=application_id)
    application.unlock()
    application.save()
    return HttpResponseRedirect(reverse('staff_view_application', args=[id]))


@login_required
@user_passes_test(staff_check)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('staff_dashboard'))
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def send_email(subject, body, recip):
    send_mail(subject, body, "capstoneproject1010@gmail.com", [recip], True)


def handle_uploaded_file(file):
    file_data = file.read().decode("utf-8")
    lines = file_data.split("\n")
    for line in lines:
        data = line.strip().split(',')
        send_email(data[1] + ": Please register for the CS application portal", "You have applied centrally at UCT for "
                   + data[0] + ",but should still complete your application on the CS portal. Follow this link to creat"
                               "e an account: http://ec2-18-222-140-131.us-east-2.compute.amazonaws.com:8000/", data[2])
