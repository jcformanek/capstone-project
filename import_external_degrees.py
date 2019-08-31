import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CapstoneProject.settings')

import django
django.setup()

from applications.models import *

external_degrees_filename = "external_degrees.txt"
uct_degrees_filename = "uct_degrees.txt"

COUNTRIES = ['Licence', 'Magister', 'Bacharel', 'Licenciado', 'Doutorado', 'Bachelor degree', 'Bachelor degree (Honours)',
                         'Master\'s degree']
EXTERNAL_DEGREE_TYPES = ['Algeria', 'Angola', 'Australia']

def add_external_degree(country, degree_type):
    d = ExternalDegree.objects.get_or_create(country=country, type=degree_type)[0]
    d.save()
    return d


def add_uct_degree(degree_name):
    d = UCTDegree.objects.get_or_create(name=degree_name)[0]
    d.save()
    return d


def populate_external_degrees():
    f = open(external_degrees_filename, 'r')
    for line in f:
        data = line.strip().split(",")
        if data[0] in COUNTRIES.countries and data[1] in EXTERNAL_DEGREE_TYPES.types:
            add_external_degree(data[0], data[1])
    f.close()


def populate_uct_degrees():
    f = open(uct_degrees_filename, 'r')
    for line in f:
        data = line.strip().split(",")
        uct_degree = add_uct_degree(data[0])
        for i in range(1, len(data[1:]), 2):
            external_degree = ExternalDegree.objects.get(country=data[i], type=data[i+1])
            uct_degree.accepted_qualifications.add(external_degree)


if __name__ == '__main__':
    print("Starting population script...")
    populate_external_degrees()
    populate_uct_degrees()