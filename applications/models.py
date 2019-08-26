from django.db import models
from users.models import *
from postgrad.models import *

EXTERNAL_DEGREE_TYPES = [('Licence','Licence'),('Magister','Magister'),('Bacharel','Bacharel'),(' Licenciado', 'Licenciado'),
                         ('Doutorado','Doutorado'),('Bachelor degree','Bachelor degree'),
                         ('Bachelor degree (Honours)','Bachelor degree (Honours)'),('Master’s degree','Master’s degree')]

COUNTRIES = [('Algeria','Algeria'), ('Angola','Angola'), ('Australia','Australia')]

class UCTDegree(models.Model):
    name = models.CharField(max_length=100)
    accepted_qualifications = models.ManyToManyField

    def __str__(self):
        return self.name


class ExternalDegree(models.Model):
    type = models.CharField(choices=EXTERNAL_DEGREE_TYPES, max_length=100)
    country = models.CharField(choices=COUNTRIES, max_length=100)


class Application(models.Model):
    postgrad_profile = models.ForeignKey(PostgradProfile, on_delete=models.CASCADE)
    degree = models.ForeignKey(UCTDegree, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default="Pending")

    def __str__(self):
        return self.degree.name + " | " + self.status

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




