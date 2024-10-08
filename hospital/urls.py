from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),

    path('', views.home, name = 'home'),

    path('account/', views.accountSettings, name="account"),

    path('patients/', views.patient_list, name = 'patient_list'),
    path('patients/addpatient', views.add_patient, name = 'add_patient'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('appointment/', views.patient_appointment, name="patient_appointment"),

    path('contact/', views.contact_page, name='contact'),
    path('reviews/', views.reviews_page, name='reviews'),

    path('blog/', views.blog_list, name='blog_list'),
    path('blog/new/', views.new_post, name='new_post'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
]