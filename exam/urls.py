from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.Exam,name="Exam"),
    path('Result',views.Result,name="Result"),
    path('Submit',views.Submit,name="Submit"),
    path('online_mcq', views.online_mcq, name="online_mcq")
    
]