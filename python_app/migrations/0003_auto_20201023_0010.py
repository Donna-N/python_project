# Generated by Django 2.2.4 on 2020-10-23 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('python_app', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('associated_doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors_note', to='python_app.Doctor')),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belong', to='python_app.Patient')),
                ('commented', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='python_app.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]