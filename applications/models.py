from django.db import models
from users.models import *

class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):
    postgrad_profile = models.ForeignKey(PostgradProfile, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default="Pending")

    def update_status(self):
        if self.is_rejected and not self.is_accepted:
            self.status = "Rejected"
        elif self.is_accepted and not self.is_rejected:
            self.status = "Accepted"
        elif not self.is_accepted and not self.is_rejected:
            self.status = "Pending"

    def accept(self):
        self.is_accepted = True
        self.is_rejected = False
        self.update_status()

    def reject(self):
        self.is_rejected = True
        self.is_accepted = False
        self.update_status()

    def pending(self):
        self.is_rejected, self.is_accepted = False
        self.update_status()

