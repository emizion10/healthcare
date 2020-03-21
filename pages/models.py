from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.admin.widgets import AdminDateWidget
import uuid 

GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)

USER_TYPE_CHOICES = (
      (1, 'patient'),
      (2, 'doctor'),
      (3, 'hospital'),
      (4,'admin'),
  )

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
	# REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


  
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
	age=models.IntegerField(blank=True)
	height=models.DecimalField(max_digits=5, decimal_places=2,blank=True)
	weight=models.DecimalField(max_digits=6, decimal_places=2,blank=True)
	bloodgroup = models.CharField(choices=bloodgroup_choices, max_length=12, default='-', blank=True)
	place=models.CharField(max_length=50,blank=True)
	imagefile=models.ImageField(upload_to='patient/',default="default.jpg",blank=True)


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
	imagefile=models.ImageField(upload_to='doctor/',default="default.jpg",blank=True)

	# city = models.CharField(max_length=255)
	# location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
	# loc=LocationField()


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
	imagefile=models.ImageField(upload_to='hospital/',blank=True)
	# city = models.CharField(max_length=255)
	# location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
	# loc=LocationField()

	def __str__(self):
		return self.name


