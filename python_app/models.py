from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['email'] = "Invalid Email/Password!"

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"

        if (postData['password']!= postData['confirm_password']):
            errors['confirm_password'] = "Password Confirm did not match"

        user = User.objects.filter(email=postData['email'])
        if(len(user)> 0):
            errors['email_password'] = 'Email/Password is incorrect.'
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])

        if len(user)== 0:
            errors['email_password'] = "Email/password is incorrect."

        else:
            if bcrypt.checkpw(
                postData['password']. encode(), user[0].password.encode()
            )!= True:
                errors['email_password'] = "Email/Password is incorrect"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    #caregivers
    #comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    known_as_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    caregiver = models.ManyToManyField(User, related_name = "caregivers")
    #treater
    #belong
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DoctorManager(models.Manager):
    def doctor_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "A first name must consist of at least 2 characters"        
        if len(postData['last_name']) < 2:
            errors["last_name"] = "A last name must consist of at least 2 characters"
        if len(postData['location']) < 1:
            errors["location"] = "A location must be provided"
        if len(postData['phone']) < 10:
            errors["phone"] = "A phone number must include at least 10 digits (please include area code)"
        if len(postData['network']) < 1:
            errors["network"] = "A network must be provided"
        if len(postData['specialty']) < 1:
            errors["specialty"] = "A specialty must be provided"
        return errors

class Doctor(models.Model):
    title = models.CharField(max_length = 255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    location = models.CharField(max_length = 255)
    phone = models.CharField(max_length=12)
    network = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    treating = models.ManyToManyField(Patient, related_name= "treater")
    #meds
    #doctors_note
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DoctorManager()

class MedicineManager(models.Manager):
    def medicine_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name_on_bottle']) < 2:
            errors["name_on_bottle"] = "A name must consist of at least 2 characters"        
        if len(postData['other_names']) < 2:
            errors["other_names"] = "Please provide at least one alternate name"
        if len(postData['we_call_it']) < 2:
            errors["we_call_it"] = "Please provide a name we use"
        if len(postData['used_for']) < 1:
            errors["used_for"] = "A use must be provided"
        if len(postData['dose']) < 1:
            errors["dose"] = "A dose must be provided"
        if len(postData['frequency']) < 1:
            errors["frequency"] = "A frequency must be provided"
        return errors

class Medicine(models.Model):
    name_on_bottle=models.CharField(max_length = 255)
    other_names= models.CharField(max_length = 255)
    we_call_it = models.CharField(max_length=255)
    used_for= models.CharField(max_length = 255)
    dose = models.CharField(max_length = 255)
    frequency = models.CharField(max_length = 255)
    prescriber = models.ManyToManyField(Doctor, related_name = 'meds')
    prescribed_to = models.ManyToManyField(Patient, related_name = 'my_meds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MedicineManager()

class DoctorComment(models.Model):
    commented = models.ForeignKey(User,related_name = 'comments',
    on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(Patient, related_name = 'belong', on_delete = models.CASCADE)
    associated_doctor = models.ForeignKey(Doctor, related_name = "doctors_note", on_delete = models.CASCADE)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)