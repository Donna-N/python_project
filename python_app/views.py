from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

#login page (index.html)
def index(request):
    return render(request,'index.html')

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password= pw_hash
        )
        request.session['uuid'] = user.id
    return redirect('/home')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['uuid'] = user.id
        return redirect("/home")

#home page (home.html)
def home(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = { 
        'userid' : User.objects.get(id=request.session['uuid']),
        'first_patient' : Patient.objects.filter(caregiver=request.session['uuid']).first(),
        'patients' : Patient.objects.filter(caregiver=request.session['uuid']),
        'doctors' : Doctor.objects.all(),
    }
    return render(request,'home.html', context)

def choose_patient(request):
    print ("I'm here")
    current_patient = Patient.objects.get(id=request.POST['patient_select'])
    print(current_patient)
    return redirect(f'/dashboard/{current_patient.id}')

def dashboard(request, patient_id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'userid' : User.objects.get(id=request.session['uuid']),
        'this_patient' : Patient.objects.get(id=patient_id),
        'patients' : Patient.objects.filter(caregiver=request.session['uuid']),
        'all_doctors' : Doctor.objects.all(),
        'all_comments': DoctorComment.objects.filter(belongs_to=patient_id).order_by('-created_at'),
        'medications': Medicine.objects.filter(prescribed_to=patient_id)
    }
    return render(request,'dashboard.html', context)

def doctors(request, patient_id):
    context = {
        'userid' : User.objects.get(id=request.session['uuid']),
        'current_patient' : Patient.objects.get(id=patient_id),
        'all_doctors' : Doctor.objects.all(),
    }
    return render(request,'doctors.html', context)

def add_doctor(request, patient_id):
    errors = Doctor.objects.doctor_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return HttpResponseRedirect (request.META.get('HTTP_REFERER'))
    else:
        doctor = Doctor.objects.create(
            title = request.POST ['title'],
            first_name = request.POST ['first_name'],
            last_name = request.POST ['last_name'],
            location = request.POST ['location'],
            phone = request.POST ['phone'],
            network = request.POST ['network'],
            specialty = request.POST ['specialty'],
        )
        this_doctor = Doctor.objects.last()
        this_patient = Patient.objects.get(id=patient_id)
        this_doctor.treating.add(this_patient)
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def add_doctor_relationship(request, patient_id, doctor_id):
    this_doctor = Doctor.objects.get(id = doctor_id)
    print(f'this doctor {this_doctor}')
    this_patient = Patient.objects.get(id=patient_id)
    print(f'this patient {this_patient}')
    this_doctor.treating.add(this_patient)
    return redirect (f'/dashboard/{patient_id}')

def remove_doctor_relationship(request, patient_id, doctor_id):
    this_doctor = Doctor.objects.get(id = doctor_id)
    this_patient = Patient.objects.get(id=patient_id)
    this_doctor.treating.remove(this_patient)
    return redirect (f'/dashboard/{patient_id}')

def doctor_details(request, doctor_id, patient_id):
    context = {
        'userid' : User.objects.get(id=request.session['uuid']),
        'current_patient' : Patient.objects.get(id=patient_id),
        'this_doctor' : Doctor.objects.get(id=doctor_id),
        'doc_comments': DoctorComment.objects.filter(associated_doctor=doctor_id).filter(belongs_to=patient_id).order_by('-created_at')
    }
    return render(request,"doctor_details.html", context)

def create_post(request, doctor_id, patient_id):
    logged_user = User.objects.get(id=request.session['uuid'])
    belongs = Patient.objects.get(id = patient_id)
    associated = Doctor.objects.get(id = doctor_id)
    DoctorComment.objects.create(
        commented= logged_user,
        belongs_to = belongs,
        associated_doctor = associated,
        message= request.POST['message']
    )
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def delete_comment(request, comment_id):
    to_delete = DoctorComment.objects.get(id = comment_id)
    to_delete.delete()
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def caregivers(request):
    return render(request,'crew.html')

def medications(request, patient_id):
    if 'uuid' not in request.session:
        return redirect('/')
    else:
        context = {
            'userid' : User.objects.get(id=request.session['uuid']),
            'current_patient' : Patient.objects.get(id=patient_id),
            'patients' : Patient.objects.filter(caregiver=request.session['uuid']),
            'all_doctors' : Doctor.objects.all(),
            'all_medicines': Medicine.objects.filter(prescribed_to=patient_id),
            'prescriber' : Medicine.objects.all()
        }
    return render(request,'medications.html', context)

def add_medication(request, patient_id):
    errors = Medicine.objects.medicine_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return HttpResponseRedirect (request.META.get('HTTP_REFERER'))
    else:
        medication = Medicine.objects.create(
            name_on_bottle = request.POST ['name_on_bottle'],
            other_names = request.POST ['other_names'],
            we_call_it = request.POST ['we_call_it'],
            used_for = request.POST ['used_for'],
            dose = request.POST ['dose'],
            frequency = request.POST ['frequency'],
        )
        this_doctor = Doctor.objects.get(id=request.POST['prescriber'])
        print(this_doctor)
        this_medicine = Medicine.objects.last()
        this_patient = Patient.objects.get(id=patient_id)
        this_medicine.prescribed_to.add(this_patient)
        this_medicine.prescriber.add(this_doctor)
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def medication_details(request, medicine_id, patient_id):
    context = {
        'userid' : User.objects.get(id=request.session['uuid']),
        'current_patient' : Patient.objects.get(id=patient_id),
        'this_medicine' : Medicine.objects.get(id=medicine_id),
    }
    return render(request,"medication_details.html", context)

def patient (request):
    return render(request,'patient.html')

def logout(request):
    request.session.flush()
    return redirect('/')

