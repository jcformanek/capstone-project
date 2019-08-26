from django import forms


class CreateProfileForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    student_number = forms.CharField(label="Student Number", max_length=9)