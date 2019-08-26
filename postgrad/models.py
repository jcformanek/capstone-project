from django.db import models
from users.models import *


class PostgradProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='postgrad_profile')
    student_number = models.CharField(max_length=9, unique=True)
