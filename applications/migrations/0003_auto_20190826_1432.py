# Generated by Django 2.2.4 on 2019-08-26 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20190826_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postgradprofile',
            name='qualification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='applications.ExternalDegree'),
        ),
    ]