# Generated by Django 2.2.4 on 2020-10-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_app', '0003_auto_20201023_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='we_call_it',
            field=models.CharField(default='name on bottle', max_length=255),
            preserve_default=False,
        ),
    ]