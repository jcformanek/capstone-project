from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from applications.models import UCTDegree, CustomUser, ExternalDegree, Application
from import_external_degrees import ExternalDegreeTypes, Countries

EXTERNAL_DEGREE_TYPES = ExternalDegreeTypes().types
COUNTRIES = Countries().countries


class NewApplicationForm(forms.Form):
    degree = forms.ModelChoiceField(queryset=UCTDegree.objects.all())
    pdf = forms.FileField()

    class Meta:
        model = Application
        fields = ('degree', 'pdf')


class CreateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    student_number = forms.CharField(label="Student Number", max_length=9)

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email')


class QualificationForm(forms.Form):
    external_degree = forms.ModelChoiceField(ExternalDegree)

    def __init__(self, country=None,**kwargs):
        super(QualificationForm, self).__init__(**kwargs)
        if country:
            self.fields['external_degree'].queryset = ExternalDegree.objects.filter(country=country)


class QualificationCountryForm(forms.Form):
    country = forms.CharField(widget=forms.Select(choices=COUNTRIES))
