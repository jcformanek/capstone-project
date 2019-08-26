from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from applications.models import UCTDegree, CustomUser, ExternalDegree

EXTERNAL_DEGREE_TYPES = ['Licence', 'Magister', 'Bacharel', 'Licenciado', 'Doutorado', 'Bachelor degree', 'Bachelor degree (Honours)',
                         'Master\'s degree']

COUNTRIES = ['Algeria', 'Angola', 'Australia']

class NewApplicationForm(forms.Form):
    degree = forms.ModelChoiceField(queryset=UCTDegree.objects.all())

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