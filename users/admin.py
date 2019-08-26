from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from postgrad.models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','is_postgrad', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)