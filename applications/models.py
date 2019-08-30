from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_postgrad = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class ExternalDegree(models.Model):
    type = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country + " " + self.type


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

class PostgradProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='postgrad_profile')
    student_number = models.CharField(max_length=9, unique=True)
    qualification = models.ForeignKey(ExternalDegree, on_delete=models.CASCADE, blank=True, null=True)

class StaffProfile(Profile):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_number = models.CharField(max_length=9, unique=True)


class UCTDegree(models.Model):
    name = models.CharField(max_length=100)
    accepted_qualifications = models.ManyToManyField(ExternalDegree)

    def __str__(self):
        return self.name


class Application(models.Model):
    postgrad_profile = models.ForeignKey(PostgradProfile, on_delete=models.CASCADE)
    degree = models.ForeignKey(UCTDegree, on_delete=models.CASCADE)
    pdf = models.FileField("PDF Upload", blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default="Pending")
    reason = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.degree.name + " | " + self.status + " | Comment: " + self.reason

    def update_status(self):
        if self.is_rejected and not self.is_accepted:
            self.status = "Rejected"
        elif self.is_accepted and not self.is_rejected:
            self.status = "Accepted"
        elif not self.is_accepted and not self.is_rejected:
            self.status = "Pending"

    def update_reason(self, reason):
        self.reason = reason

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