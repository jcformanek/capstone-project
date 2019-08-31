from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from applications.models import UCTDegree, CustomUser, ExternalDegree, Application, Qualification

EXTERNAL_DEGREE_TYPES = ['Licence', 'Magister', 'Bacharel', 'Licenciado', 'Doutorado', 'Bachelor degree', 'Bachelor degree (Honours)',
                         'Master\'s degree']
countries = ['Algeria', 'Angola', 'Australia']

COUNTRIES = []
for c in countries:
    COUNTRIES.append((c,c))


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
    external_degree = forms.ModelChoiceField(ExternalDegree.objects.all())
    university = forms.CharField(max_length=100)
    min_years = forms.IntegerField()
    thesis = forms.BooleanField()

    class Meta:
        model = Qualification
        fields = ("external_degree", "university", "min_years", "thesis")


class QualificationCountryForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRIES)
