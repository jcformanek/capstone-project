# users/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, PostgradProfile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email')


class CreateProfileForm(forms.Form):
    student_number = forms.CharField(label="Student Number", max_length=9)
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
