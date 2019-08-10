from django.forms import forms, ModelChoiceField
from applications.models import Degree


class NewApplicationForm(forms.Form):
    degree = ModelChoiceField(queryset=Degree.objects.all())