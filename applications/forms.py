from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from applications.models import *

EXTERNAL_DEGREE_TYPES = ['Licence', 'Magister', 'Bacharel', 'Licenciado', 'Doutorado', 'Bachelor degree', 'Bachelor degree (Honours)',
                         'Master\'s degree']
countries = ['Algeria', 'Angola', 'Australia',"Argentina",'Austria','Botswana','Brazil','Canada']

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


class ReasonForm(forms.Form):
    reason = forms.CharField(max_length=1000)


class EditProfileForm(ModelForm):
    class Meta():
        model = PostgradProfile
        fields = "__all__"


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
        fields = ['student_number', 'title', 'first_name', 'last_name', 'current_country',
                  'current_city', 'citizenship_country']


class CreateRSAPostgradProfileForm(ModelForm):
    class Meta:
        model = PostgradProfile
        fields = ['student_number', 'title', 'first_name', 'last_name', 'race', 'current_country','current_city']


class UploadFileForm(forms.Form):
    file = forms.FileField()


