from django.db import models
from django_mysql.models import ListTextField,ListCharField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.admin.widgets import AdminDateWidget
import uuid 
from places.fields import PlacesField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from datetime import datetime

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'not specified'),
)

USER_TYPE_CHOICES = (
      (1, 'patient'),
      (2, 'doctor'),
      (3, 'hospital'),
      (4,'admin'),
      (5,'laboratory'),
      
  )

ACCESS_CHOICES = (
	('public','public'),
	('private','private'),
	('custom','custom'),
)


spec_choices = (("Hypertensiology","Hypertensiology"),
	("Surgery","Surgery"),
	("Gastroenterology","Gastroenterology"),
	("Traumatology","Traumatology"),
	("Ophthalmology","Ophthalmology"),
	("Toxicology","Toxicology"),
	("Orthopedics","Orthopedics"),
	("Dermatology","Dermatology"),
	("Infectiology","Infectiology"),
	("Endocrinology","Endocrinology"),
	("Pulmonology","Pulmonology"),
	("Urology","Urology"),
	("Cardiology","Cardiology"),
	("Nephrology","Nephrology"),
	("Hematology","Hematology"),
	("Laryngology/ENT","Laryngology/ENT"),
	("Gynecology","Gynecology"),
	("Psychiatry","Psychiatry"),
	("Oncology","Oncology"),
	("Allergology","Allergology"),
	("Neurology","Neurology"),
	("Rheumatology","Rheumatology"),
	("Venereology","Venereology"),
	("Angiology","Angiology"),
	("Internal Medicine","Internal Medicine"),
	("Other","Other"),
	("Dentistry","Dentistry"),
	("Diabetology","Diabetology"))


class MyAccountManager(BaseUserManager):
	def create_user(self, username, password=None):
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, password):
		user = self.create_user(
			# email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user




class MyUser(AbstractBaseUser):
  
	
	username= models.CharField(max_length=30,unique=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin= models.BooleanField(default=False)
	is_active= models.BooleanField(default=True)
	is_staff= models.BooleanField(default=False)
	is_superuser= models.BooleanField(default=False)
	user_type= models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=4)

	USERNAME_FIELD = 'username'

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True



class Follow(models.Model):
    following = models.ForeignKey('pages.Doctor',on_delete=models.CASCADE)
    limit = models.Q(app_label = 'pages', model = 'Doctor') | models.Q(app_label = 'pages', model = 'Patient')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    follower = GenericForeignKey('content_type', 'object_id')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.follower) + ':' + str(self.following)




  
class Patient(models.Model):
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
	id=models.BigAutoField(primary_key=True)
	username= models.OneToOneField(MyUser,on_delete=models.CASCADE)
	regid=models.UUIDField(default = uuid.uuid4,editable = False)
	pname=models.CharField(max_length=50)
	gender=models.IntegerField(choices=GENDER_CHOICES,blank=True)
	dob = models.DateField(null=True, blank=True)
	# age=models.IntegerField(blank=True)
	height=models.DecimalField(max_digits=5, decimal_places=2,blank=True)
	weight=models.DecimalField(max_digits=6, decimal_places=2,blank=True)
	bloodgroup = models.CharField(choices=bloodgroup_choices, max_length=12, default='-', blank=True)
	place=models.CharField(max_length=100,blank=True)
	imagefile=models.ImageField(upload_to='patient/',default="default.jpg",blank=True,null=True)
	email = models.EmailField(max_length=254,blank=True)
	contact = models.CharField(max_length=14,blank=True)
	aadhaar = models.CharField(max_length=12,blank=True)
	follower = GenericRelation(Follow,related_query_name='patient')
 
	@property
	def age(self):
		return int((datetime.now().date() - self.dob).days / 365.25)

	def __str__(self):
		return self.pname

class Doctor(models.Model):
	id=models.BigAutoField(primary_key=True)
	username= models.OneToOneField(MyUser,on_delete=models.CASCADE)
	regid = models.CharField(max_length=60,unique=True) 
	dname=models.CharField(max_length=50)
	dob = models.DateField(null=True, blank=True)
	gender=models.IntegerField(choices=GENDER_CHOICES,blank=True)
	spec=models.CharField(max_length=50,blank=True)
	hos=models.CharField(max_length=150,blank=True)
	imagefile=models.ImageField(upload_to='doctor/',default="default.jpg",blank=True,null=True)
	location = PlacesField()
	follower = GenericRelation(Follow,related_query_name='doctor')
	state=models.CharField(max_length=20,blank=True)
	email = models.EmailField(max_length=254,blank=True)
	contact = models.CharField(max_length=14,blank=True)
	aadhaar = models.CharField(max_length=12,blank=True)
	


	def __str__(self):
		return self.dname

class Hospital(models.Model):
	id=models.BigAutoField(primary_key=True)
	username= models.OneToOneField(MyUser,on_delete=models.CASCADE)
	regid=models.CharField(max_length=50,unique=True)
	name=models.CharField(max_length=50)
	category=models.CharField(max_length=10,blank=True)
	spec=models.TextField(blank=True)
	services=models.TextField(blank=True)
	email=models.EmailField(blank=True)
	url=models.URLField(blank=True)
	contact = models.CharField(max_length=14,blank=True)
	address=models.TextField(blank=True)
	description = models.TextField(blank=True)
 
	imagefile=models.ImageField(upload_to='hospital/',blank=True,null=True)
	location = PlacesField()
	
	def __str__(self):
		return self.name

class Laboratory(models.Model):
	id=models.BigAutoField(primary_key=True)
	username = models.OneToOneField(MyUser,on_delete=models.CASCADE)
	regid=models.CharField(max_length=50,unique=True)
	name=models.CharField(max_length=50)
	email=models.EmailField(blank=True)
	contact = models.CharField(max_length=14,blank=True)
	services=models.TextField(blank=True)
	
	address=models.TextField(blank=True)
	description = models.TextField(blank=True)
 
 
	def __str__(self):
		return self.name


class MedicalRecord(models.Model):
	id=models.BigAutoField(primary_key=True)
	patient_id = models.ForeignKey(Patient, verbose_name="patient",on_delete=models.CASCADE)
	doctor_id = models.ForeignKey(Doctor, verbose_name="doctor",on_delete=models.CASCADE)
	condition = models.CharField(max_length=100,blank=True)
	permission = models.CharField(choices=ACCESS_CHOICES,max_length=10,blank=True)
	access = models.CharField(max_length=100,blank=True)	
	diagnosis = ListTextField(
		base_field = models.CharField(max_length=100,blank=True),
	)
	procedures = ListTextField(
		base_field = models.CharField(max_length=100,blank=True),
	)
	prescription = ListTextField(
		base_field = models.CharField(max_length=100,blank=True),
	)
	description = models.TextField(blank=True)
	visit_date = models.DateTimeField(auto_now_add=True, verbose_name="Visit Date")
    
	def __str__(self):
		return u'%s  %s' % (self.patient_id, self.id)


class LaboratoryRecord(models.Model):
	id=models.BigAutoField(primary_key=True)
	patient_id = models.ForeignKey(Patient, verbose_name="patient",on_delete=models.CASCADE)
	lab_id = models.ForeignKey(Laboratory, verbose_name="laboratory",on_delete=models.CASCADE)
	procedure = models.CharField(max_length=100,blank=True)
	description = models.TextField(blank=True)
	upload_file = models.FileField(upload_to='labrecords/',blank=True,null=True)
	medrec = models.ForeignKey(MedicalRecord,on_delete=models.CASCADE)
	add_date = models.DateTimeField(auto_now_add=True, verbose_name="Visit Date")
 
	def __str__(self):
		return u'%s  %s' % (self.patient_id, self.id)

    

class Review(models.Model):
    rating = models.IntegerField(blank=False)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Patient, verbose_name="patient",on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, verbose_name="doctor",on_delete=models.CASCADE)
    spec=models.CharField(choices=spec_choices,max_length=50,default='Other')
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return u'%s  %s' % (self.doctor, self.id)


class Post(models.Model):
    title = models.CharField(max_length=100,blank=True)
    content = models.TextField(blank=True)
    image=models.ImageField(upload_to='posts/',blank=True,null=True)
    author = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    
PREFERENCE_CHOICES = (
	(1,'like'),
	(0,'dislike')
)
class Preference(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    value = models.IntegerField(choices=PREFERENCE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)
    
    
class Comments(models.Model):
	id=models.BigAutoField(primary_key=True)
	comment = models.CharField(max_length=140,blank=True)
	post = models.ForeignKey(Post,on_delete=models.CASCADE)
	author = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
    
	def __str__(self):
		return str(self.post) +':'+str(self.author)+':'+str(self.id)


class Messages(models.Model):
    sender=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='sender')
    reciever=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='reciever')
    subject = models.CharField(max_length=50,blank=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.sender) + ':' + str(self.reciever)+':'+str(self.date)
    
    
class Education(models.Model):
    user = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=150,null=True,blank=True)
    institute_name = models.CharField(max_length=150, null=True, blank=True)
    date_start = models.CharField(null=True,blank=True,max_length=25)
    date_end = models.CharField(null=True,blank=True,max_length=25)
    description = models.TextField(null=True,blank=True,max_length=1000)
    
    def __str__(self):
        return str(self.user) + ':' + str(self.degree_name)
    
    

class Experience(models.Model):
    user = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    designation = models.CharField(max_length=150,null=True,blank=True)
    hospital_name = models.CharField(max_length=150, null=True, blank=True)
    date_start = models.CharField(null=True,blank=True,max_length=25)
    date_end = models.CharField(null=True,blank=True,max_length=25)
    description = models.TextField(null=True,blank=True,max_length=1000)
    
    def __str__(self):
        return str(self.user) + ':' + str(self.hospital_name)