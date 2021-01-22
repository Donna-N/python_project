# Generated by Django 2.2.4 on 2020-10-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_app', '0005_medicine_prescribed_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='prescriber',
        ),
        migrations.AddField(
            model_name='medicine',
            name='prescriber',
            field=models.ManyToManyField(related_name='meds', to='python_app.Doctor'),
        ),
    ]