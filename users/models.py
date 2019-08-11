from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_postgrad = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class PostgradProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='postgrad_profile')
    student_number = models.CharField(max_length=9, unique=True)

class StaffProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_number = models.CharField(max_length=9, unique=True)

