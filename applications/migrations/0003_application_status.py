# Generated by Django 2.2.4 on 2019-08-11 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20190811_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(default='Pending', max_length=10),
        ),
    ]
