from django.db import models
from users.models import *

class StaffProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_number = models.CharField(max_length=9, unique=True)
