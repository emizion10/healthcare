from django.urls import path
from . import views
from .views import *

urlpatterns = [

	path('login/', views.login_view, name='login'),
	path('',views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('addp/',AddPatient.as_view(), name='addp'),
    path('addd/',AddDoctor.as_view(), name='addd'),
    path('doctorprofile/',DoctorProfile.as_view(), name='doctorprofile'),
    path('patientprofile/',PatientProfile.as_view(), name='patientprofile'),
    
    

 ]
