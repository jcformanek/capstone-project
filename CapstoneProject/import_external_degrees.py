import os
from applications.models import ExternalDegree
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CapstoneProject.settings')
django.setup()


def add_degree(country, type):
    d = ExternalDegree.objects.get_or_create(country=country, type=type)[0]
    d.save()
    return d


def populate():
    add_degree('Licence','Algeria')
    add_degree('Magister', 'Algeria')


if __name__ == '__main__':
    print("Starting population script...")
    populate()