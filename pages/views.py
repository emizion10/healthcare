from . models import *
from . forms import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.shortcuts import render_to_response, redirect,render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied


@login_required(login_url='login')
def home(request):
	return render(request,'pages/home.html')

def index(request):
	return render(request,'pages/index.html')

def capture(request):
	return render(request,'pages/capture2.html')


class MyPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def dispatch(self, request, *args, **kwargs):
    	if not request.user.is_authenticated:
    		return redirect('login')
    	else:
        	user_test_result = self.get_test_func()()
        	if not request.user.is_authenticated or not user_test_result:
        		return HttpResponse('<h2> Permission Denied ! </h2>')
        	return super().dispatch(request, *args, **kwargs)


def login_view(request):
	context = {}
	
	user = request.user
	if user.is_authenticated: 
		return redirect('/home/')

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)

			if user:
				login(request, user)
				return redirect("/home/")
			
	else:
		form = UserAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "registration/login.html", {'form':form})


class AddPatient(MyPermissionMixin,CreateView):

	raise_exception = True
	login_url = "/login/"
	model=MyUser
	template_name='pages/addpatient.html'
	form_class=PatientForm
	success_url = '/home/'

	def test_func(self):
		return (self.request.user.user_type==2)

	def form_valid(self, form):
		usr = form.save(commit=False)
		username = form.cleaned_data['username']
		pname = form.cleaned_data['pname']
		gender=form.cleaned_data['gender']
		dob = form.cleaned_data['dob']
		age=form.cleaned_data['age']
		height=form.cleaned_data['height']
		weight=form.cleaned_data['weight']
		bloodgroup=form.cleaned_data['bloodgroup']
		place=form.cleaned_data['place']
		imagefile=self.request.FILES['imagefile']
		password = form.cleaned_data['password']
		usr.set_password(password)
		usr.user_type=1
		usr.save()

		Patient.objects.create(username=usr,pname=pname,gender=gender,dob=dob,age=age,height=height,weight=weight,bloodgroup=bloodgroup,place=place,imagefile=imagefile)

		return super(AddPatient, self).form_valid(form)


class AddDoctor(MyPermissionMixin,CreateView):
	raise_exception = True
	login_url = "/login/"
	model=MyUser
	template_name='pages/adddoctor.html'
	form_class=DoctorForm
	success_url = '/home/'

	def test_func(self):
		return (self.request.user.user_type==3)

	def form_valid(self, form):
		usr = form.save(commit=False)
		username = form.cleaned_data['username']
		regid=form.cleaned_data['regid']
		dname = form.cleaned_data['dname']
		gender=form.cleaned_data['gender']
		dob = form.cleaned_data['dob']
		spec=form.cleaned_data['spec']
		hos=form.cleaned_data['hos']
		imagefile=self.request.FILES['imagefile']
		password = form.cleaned_data['password']
		usr.set_password(password)
		usr.user_type=2
		usr.save()

		Doctor.objects.create(username=usr,regid=regid,dname=dname,gender=gender,dob=dob,spec=spec,hos=hos,imagefile=imagefile)

		return super(AddDoctor, self).form_valid(form)

def logout_view(request):
	logout(request)
	return redirect("login")




