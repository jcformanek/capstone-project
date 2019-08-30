from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from applications.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(Application)
admin.site.register(UCTDegree)
admin.site.register(ExternalDegree)
admin.site.register(PostgradProfile)
admin.site.register(StaffProfile)
admin.site.register(CustomUser, CustomUserAdmin)
