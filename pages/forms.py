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
YEARS= [x for x in range(1920,2020)]

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

class PatientForm(forms.ModelForm):
      username=forms.CharField(max_length=60,label='Username')
      password = forms.CharField(widget=forms.PasswordInput,label='Password')
      pname=forms.CharField(max_length=100,label='Name')
      gender=forms.ChoiceField(choices=GENDER_CHOICES,label='Gender',required=False)
      dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),label='Date of Birth',required=False)
      age=forms.IntegerField(label='Age',required=False)
      height=forms.DecimalField(label='Height',required=False)
      weight=forms.DecimalField(label='Weight',required=False)
      bloodgroup=forms.ChoiceField(choices=bloodgroup_choices,label='Blood Group',required=False)
      place=forms.CharField(max_length=50,label='Place',required=False)
      imagefile=forms.ImageField(required=False,label='Upload Image')

      # phno = forms.CharField(max_length=20)
      class Meta():
          model = MyUser
          fields = ('username','password','pname','gender','dob','age','height','weight','bloodgroup','place','imagefile')
		

class DoctorForm(forms.ModelForm):

      spec_choices = (('Allergy and Immunology', 'Allergy and Immunology'),
            ('Anesthesiology', 'Anesthesiology'),
            ('Dermatology', 'Dermatology'),
            ('Diagnostic Radiology', 'Diagnostic Radiology'),
            ('Emergency Medicine', 'Emergency Medicine'),
            ('Family Medicine ', 'Family Medicine '),
            ('Medical Genetics', 'MedicalGenetics'),
            ('Neurology', 'Neurology'),
            ('Nuclear Medicine', 'Nuclear Medicine'),
            ('Obstetris and Gynecology', 'Obstetris and Gynecology'),
            ('Ophthalmology', 'Ophthalmology'),
            ('Pathology', 'Pathology'),
            ('Pediatrics', 'Pediatrics'),
            ('Pathology', 'Pathology'),
            ('Physical Medicine and Rehabilitation', 'Physical Medicine and Rehabilitation'),
            ('Preventative Medicine', 'Preventative Medicine'),
            ('Psychiatry', 'Psychiatry'),
            ('Radiation Oncology', 'Radiation Oncology'),
            ('Surgery', 'Surgery'),
            ('Urology', 'Urology'),

            )


      username=forms.CharField(max_length=60,label='Username')
      password = forms.CharField(widget=forms.PasswordInput,label='Password')
      regid=forms.CharField(max_length=60,label='Registration No.')
      dname=forms.CharField(max_length=100,label='Name')
      gender=forms.ChoiceField(choices=GENDER_CHOICES,required=False,label='Gender')
      dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS),required=False,label='Date of Birth')
      spec=forms.ChoiceField(choices=spec_choices,required=False,label='Specialization Area')
      hos=forms.CharField(max_length=150,required=False,label='Hospital Name')
      imagefile=forms.ImageField(required=False,label='Upload Image')
      # phno = forms.CharField(max_length=20)
      class Meta():
          model=MyUser
          fields = ('username','password','regid','dname','dob','gender','spec','hos','imagefile')

      def clean_regid(self):
        if Doctor.objects.filter(regid__iexact=self.cleaned_data['regid']):
            raise forms.ValidationError('DUPLICATE_REGID')
        return self.cleaned_data['regid']
      