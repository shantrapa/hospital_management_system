from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.home, name = 'home'),
    path('user/', views.userPage, name = "user-page"),

    path('patients/', views.patient_list, name = 'patient_list'),
    path('patients/add/', views.add_patient, name = 'add_patient'),


]