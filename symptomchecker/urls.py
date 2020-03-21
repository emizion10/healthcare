from django.urls import path
from . import views
from .views import *

urlpatterns = [

	path('',views.homesymptomchecker,name='homesymptomchecker'),
    path('profile/',views.profile,name='profile'),
    path('predict/',views.predict,name='predict'),


]