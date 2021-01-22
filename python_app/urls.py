from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('home', views.home),
    path('choose_patient', views.choose_patient),
    path('dashboard/<int:patient_id>', views.dashboard),
    path('dashboard/<int:patient_id>/doctors', views.doctors),
    path('add_doctor/<int:patient_id>', views.add_doctor),
    path('add_to_doctors/<int:patient_id>/<int:doctor_id>', views.add_doctor_relationship),
    path('remove_from_doctors/<int:patient_id>/<int:doctor_id>', views.remove_doctor_relationship),
    path('doctors/<int:patient_id>/<int:doctor_id>', views.doctor_details),
    path('post/create/<int:patient_id>/<int:doctor_id>', views.create_post),
    path('delete_comment/<int:comment_id>', views.delete_comment),
    path('caregivers', views.caregivers),
    path('dashboard/<int:patient_id>/medications', views.medications),
    path('add_medication/<int:patient_id>', views.add_medication),
    path('medicine/<int:patient_id>/<int:medicine_id>', views.medication_details),
    path('recipient', views.patient), 
    path('logout', views.logout)
]