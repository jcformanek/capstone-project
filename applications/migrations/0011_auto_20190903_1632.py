# Generated by Django 2.2.4 on 2019-09-03 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0010_auto_20190903_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgradprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postgrad_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]