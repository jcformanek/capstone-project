from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from applications.models import *

EXTERNAL_DEGREE_TYPES = ['Licence', 'Magister', 'Bacharel', 'Licenciado', 'Doutorado', 'Bachelor degree', 'Bachelor degree (Honours)',
                         'Master\'s degree']
countries = ['Algeria', 'Angola', 'Australia']

COUNTRIES = []
for c in countries:
    COUNTRIES.append((c,c))


class QualificationForm(ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'university', 'min_years', 'thesis']

    def __init__(self, country, *args, **kwargs):
        super(QualificationForm, self).__init__(*args, **kwargs)
        self.fields['degree'].queryset = ExternalDegree.objects.filter(country=country)


class NewApplicationForm(forms.Form):
    degree = forms.ModelChoiceField(queryset=UCTDegree.objects.all())
    country = forms.ChoiceField(choices=COUNTRIES)


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['degree', 'pdf']


class UploadPdfForm(forms.Form):
    pdf = forms.FileField()


class SelectUCTDegree(forms.Form):
    degree = forms.ModelChoiceField(queryset=UCTDegree.objects.all())


class CreateProfileForm(forms.Form):
    student_number = forms.CharField(label="Student Number", max_length=9)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email')


class QualificationCountryForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRIES)


class SelectCitizenshipForm(forms.Form):
    citizenship = forms.ChoiceField(choices=[('RSA-Citizen', 'RSA-Citizen'),
                                                            ("RSA-Permanent-Resident", "RSA-Permanent-Resident"),
                                                            ('International', 'International')])


class CreateInterPostgradProfileForm(ModelForm):
    class Meta:
        model = PostgradProfile
        fields = ['student_number', 'first_name', 'last_name', 'email', 'current_country',
                  'current_city', 'citizenship_country']


class CreateRSAPostgradProfileForm(ModelForm):
    class Meta:
        model = PostgradProfile
        fields = ['student_number', 'first_name', 'last_name', 'email', 'race', 'current_country','current_city']


