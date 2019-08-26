from django.forms import forms, ModelChoiceField
from applications.models import UCTDegree


class NewApplicationForm(forms.Form):
    degree = ModelChoiceField(queryset=UCTDegree.objects.all())