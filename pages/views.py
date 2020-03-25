from . models import *
from . forms import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from . decorators import *
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
from django.db.models import Q

@login_required(login_url='login')
def home(request):
    return render(request, 'pages/home.html')


def index(request):
    return render(request, 'pages/index.html')


def capture(request):
    return render(request, 'pages/capture2.html')


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
    return render(request, "registration/login.html", {'form': form})


class AddPatient(MyPermissionMixin, CreateView):

    raise_exception = True
    login_url = "/login/"
    model = MyUser
    template_name = 'pages/addpatient.html'
    form_class = PatientForm
    success_url = '/home/'

    def test_func(self):
        return (self.request.user.user_type == 2)

    def form_valid(self, form):
        usr = form.save(commit=False)
        username = form.cleaned_data['username']
        pname = form.cleaned_data['pname']
        gender = form.cleaned_data['gender']
        dob = form.cleaned_data['dob']
        age = form.cleaned_data['age']
        height = form.cleaned_data['height']
        weight = form.cleaned_data['weight']
        bloodgroup = form.cleaned_data['bloodgroup']
        place = form.cleaned_data['place']
        imagefile = self.request.FILES['imagefile']
        password = form.cleaned_data['password']
        usr.set_password(password)
        usr.user_type = 1
        usr.save()

        Patient.objects.create(username=usr, pname=pname, gender=gender, dob=dob, age=age,
                               height=height, weight=weight, bloodgroup=bloodgroup, place=place, imagefile=imagefile)

        return super(AddPatient, self).form_valid(form)


class AddDoctor(MyPermissionMixin, CreateView):
    raise_exception = True
    login_url = "/login/"
    model = MyUser
    template_name = 'pages/adddoctor.html'
    form_class = DoctorForm
    success_url = '/home/'

    def test_func(self):
        return (self.request.user.user_type == 3)

    def form_valid(self, form):
        usr = form.save(commit=False)
        username = form.cleaned_data['username']
        regid = form.cleaned_data['regid']
        dname = form.cleaned_data['dname']
        gender = form.cleaned_data['gender']
        dob = form.cleaned_data['dob']
        spec = form.cleaned_data['spec']
        hos = form.cleaned_data['hos']
        imagefile = self.request.FILES['imagefile'] if 'imagefile' in self.request.FILES else False
        if imagefile == False:
            imagefile = 'default.jpg'
        password = form.cleaned_data['password']
        usr.set_password(password)
        usr.user_type = 2
        usr.save()

        Doctor.objects.create(username=usr, regid=regid, dname=dname,
                              gender=gender, dob=dob, spec=spec, hos=hos, imagefile=imagefile)

        return super(AddDoctor, self).form_valid(form)


class DoctorProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'doctor'

    def get_object(self):
        return get_object_or_404(Doctor, username=self.request.user)

    template_name = 'pages/doctorprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 2)


class PatientProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'patient'

    def get_object(self):
        return get_object_or_404(Patient, username=self.request.user)
    
    def get_context_data(self,**kwargs):
        context = super(PatientProfile, self).get_context_data(**kwargs)
        pt = get_object_or_404(Patient,username = self.request.user)
        context['records'] = MedicalRecord.objects.filter(patient_id=pt)
        return context

    template_name = 'pages/patientprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 1)


class HospitalProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'hospital'

    def get_object(self):
        return get_object_or_404(Hospital, username=self.request.user)

    template_name = 'pages/hospitalprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 3)


class MedicalCard(PDFTemplateResponseMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'patient'

    def get_object(self):
        return get_object_or_404(Patient, username=self.request.user)

    template_name = 'pages/medicalcard.html'

    def test_func(self):
        return (self.request.user.user_type == 1)


class TreatPatient(MyPermissionMixin, TemplateView):
    raise_exception = True
    login_url = "/login/"

    template_name = 'pages/treatpatient.html'

    def test_func(self):
        return (self.request.user.user_type == 2)


@user_is_doctor
def treatpatientprofile(request):
    if request.method == 'POST':
        request.session['regid'] = request.POST['regid']
        reg = request.POST['regid']
        pt = get_object_or_404(Patient, regid=reg)
        doc = get_object_or_404(Doctor,username = request.user)
        rec = MedicalRecord.objects.filter(Q(permission='public')|Q(doctor_id=doc))
        return render(request, 'pages/patientprofile.html', {'patient': pt,'records':rec})


@user_is_doctor
def addmedicalrecord(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medrecord = form.save(commit=False)
            medrecord.permission = 'private'
            medrecord.doctor_id = get_object_or_404(
                Doctor, username=request.user)
            medrecord.patient_id = get_object_or_404(
                Patient, regid=request.session['regid'])
            medrecord.save()
            pt = get_object_or_404(Patient, regid=request.session['regid'])
            doc = get_object_or_404(Doctor,username=request.user)
            rec = MedicalRecord.objects.filter(Q(permission='public')|Q(doctor_id=doc))
            return render(request, 'pages/patientprofile.html', {'patient': pt,'records':rec})
    else:
        form = MedicalRecordForm()

    return render(request, 'pages/addmedicalrecord.html', {'forms': form})


def logout_view(request):
    logout(request)
    return redirect("login")
