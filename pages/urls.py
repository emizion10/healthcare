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
    path('hospitalprofile/',HospitalProfile.as_view(), name='hospitalprofile'),
    path('patient/medicalcard/',MC.as_view(), name='medicalcard'),
    path('treatpatient/',TreatPatient.as_view(), name='treatpatient'),
    path('treatpatient/patient',treatpatientprofile, name='patient'),
    path('treatpatient/medicalrecord',views.addmedicalrecord, name='addmedicalrecord'),
    path('medicalrecord/<int:pk>',MedicalRecordDetail.as_view(), name='medicalrecord'),
    path('medicalrecord/editpermission/',views.editpermission, name='editpermission'),
    path('viewdoctor/<slug:slug>',ViewDoctor.as_view(), name='viewdoctor'),
    path('doctorreview/',views.addreview, name='doctorreview'),
    path('myposts/',DoctorPosts.as_view(), name='myposts'),
    path('addpost/',views.addpost, name='addpost'),
    path('postdetail/<int:pk>',PostDetail.as_view(), name='postdetail'),
    path('postdetail/<int:pk>/preference/<int:value>',views.postpreference, name='postpreference'),
    path('postdetail/<int:pk>/addcomment',views.addcomment, name='addcomment'),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

 ]
