from django.urls import path
from . import views
from .views import *

urlpatterns = [

	path('login/', views.login_view, name='login'),
	path('',views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('addp/',AddPatient.as_view(), name='addp'),
    path('addd/',AddDoctor.as_view(), name='addd'),
    path('covid/',views.covid, name='covid'),
    path('diseaseprediction/',views.diseaseprediction, name='diseaseprediction'),
    
    path('patients/',PatientList.as_view(), name='patients'),
    path('changepassword/',views.change_password, name='changepassword'),
    
    path('doctorprofile/',DoctorProfile.as_view(), name='doctorprofile'),
    path('patientprofile/',PatientProfile.as_view(), name='patientprofile'),
    path('hospitalprofile/',HospitalProfile.as_view(), name='hospitalprofile'),
    path('patient/medicalcard/',MC.as_view(), name='medicalcard'),
    path('treatpatient/',TreatPatient.as_view(), name='treatpatient'),
    path('laboratory/',LabRecord.as_view(), name='laboratory'),
    path('laboratory/labpatient',views.labpatient, name='labpatient'),
    path('addlaboratoryrecord/',views.addlabrecord, name='addlaboratoryrecord'),
    path('medicalrecord/<int:pk>/doctorstreated',views.doctorstreated, name='doctorstreated'),
    
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
    path('followdoctor/<int:pk>/',views.followdoctor, name='followdoctor'),
    path('unfollowdoctor/<int:pk>/',views.unfollowdoctor, name='unfollowdoctor'),
    path('doctorlist/',DoctorList.as_view(), name='doctorlist'),
    path('sendmessage/',views.sendmessage, name='sendmessage'),
    path('viewmessage/',ViewMessage.as_view(), name='viewmessage'),
    path('deletemessage/<int:pk>',views.deletemessage, name='deletemessage'),
    path('doctorrecommend/',views.doctorrecommend, name='doctorrecommend'),
    path('predictdoctor/',views.predictdoctor, name='predictdoctor'),
    path('addeducation/',views.addeducation, name='addeducation'),
    path('addexperience/',views.addexperience, name='addexperience'),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

 ]
