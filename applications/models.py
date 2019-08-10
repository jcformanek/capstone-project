from django.db import models
from users.models import *

class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):
    postgrad_profile = models.ForeignKey(PostgradProfile, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)