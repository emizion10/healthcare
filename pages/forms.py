from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import authenticate


GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)

bloodgroup_choices = (('apos', 'A+'),
                      ('aneg', 'A-'),
                      ('bpos', 'B+'),
                      ('bneg', 'B-'),
                      ('opos', 'O+'),
                      ('oneg', 'O-'),
                      ('abpos', 'AB+'),
                      ('abneg', 'AB-'),
                      ('unspecified', '-')
                      )

state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh","Arunachal Pradesh"),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir","Jammu and Kashmir"),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttarakhand","Uttarakhand"),("Uttar Pradesh","Uttar Pradesh"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"))


YEARS = [x for x in range(1920, 2020)]


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login")


class ChangePasswordForm(forms.Form):
    # old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(label='Confirm New Password')

    def clean(self):
        if self.is_valid():
            
                
            new = self.cleaned_data['new_password']
            confirm = self.cleaned_data['confirm_password']
            if not (new==confirm):
                raise forms.ValidationError("Passwords do not Match !")


        
class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=60, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    pname = forms.CharField(max_length=100, label='Name')
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, label='Gender', required=False)
   
    height = forms.DecimalField(label='Height', required=False)
    weight = forms.DecimalField(label='Weight', required=False)
    bloodgroup = forms.ChoiceField(
        choices=bloodgroup_choices, label='Blood Group', required=False)
    place = forms.CharField(max_length=50, label='Address', required=False,widget=forms.Textarea)
    imagefile = forms.ImageField(required=False, label='Upload Image')
    email = forms.CharField(max_length=100, label='Email')
    aadhaar = forms.CharField(max_length=100, label='Aadhaar')
    contact = forms.CharField(max_length=100, label='Contact')


    
    class Meta():
        model = MyUser
        fields = ('username', 'password', 'pname', 'gender',
                  'height', 'weight', 'bloodgroup', 'place', 'imagefile','email','aadhaar','contact')


class DoctorForm(forms.ModelForm):

    spec_choices = (("Hypertensiology", "Hypertensiology"),
                    ("Surgery", "Surgery"),
                    ("Gastroenterology", "Gastroenterology"),
                    ("Traumatology", "Traumatology"),
                    ("Ophthalmology", "Ophthalmology"),
                    ("Toxicology", "Toxicology"),
                    ("Orthopedics", "Orthopedics"),
                    ("Dermatology", "Dermatology"),
                    ("Infectiology", "Infectiology"),
                    ("Endocrinology", "Endocrinology"),
                    ("Pulmonology", "Pulmonology"),
                    ("Urology", "Urology"),
                    ("Cardiology", "Cardiology"),
                    ("Nephrology", "Nephrology"),
                    ("Hematology", "Hematology"),
                    ("Laryngology/ENT", "Laryngology/ENT"),
                    ("Gynecology", "Gynecology"),
                    ("Psychiatry", "Psychiatry"),
                    ("Oncology", "Oncology"),
                    ("Allergology", "Allergology"),
                    ("Neurology", "Neurology"),
                    ("Rheumatology", "Rheumatology"),
                    ("Venereology", "Venereology"),
                    ("Angiology", "Angiology"),
                    ("Internal Medicine", "Internal Medicine"),
                    ("Other", "Other"),
                    ("Dentistry", "Dentistry"),
                    ("Diabetology", "Diabetology"))

    us = forms.CharField(max_length=60, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    regid = forms.CharField(max_length=60, label='Registration No.')
    dname = forms.CharField(max_length=100, label='Name')
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, label='Gender')
    
    spec = forms.ChoiceField(choices=spec_choices,
                             required=False, label='Specialization Area')
    # hos = forms.CharField(max_length=150, required=False,
    #                       label='Hospital Name')
    imagefile = forms.ImageField(required=False, label='Upload Image')
    state = forms.ChoiceField(choices=state_choices,required=True, label='State')
    email = forms.CharField(max_length=100, label='Email')
    aadhaar = forms.CharField(max_length=100, label='Aadhaar')
    contact = forms.CharField(max_length=100, label='Contact')




    class Meta():
        model = Doctor
        fields = ('us', 'password', 'regid', 'dname'
                  , 'gender', 'spec', 'imagefile','state','email','aadhaar','contact', 'location')

    def clean_regid(self):
        if Doctor.objects.filter(regid__iexact=self.cleaned_data['regid']):
            raise forms.ValidationError('DUPLICATE_REGID')
        return self.cleaned_data['regid']


class MedicalRecordForm(forms.ModelForm):

    class Meta():
        model = MedicalRecord
        fields = ('condition', 'prescription',
                  'procedures', 'description', 'diagnosis')


class ReviewForm(forms.ModelForm):

    class Meta():
        model = Review
        fields = ('rating', 'description')


class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('title', 'content', 'image')
