from django.urls import path
from . import views
from .views import (
    dashboard, 
    patient_list, 
    patient_detail,
    add_patient,
    add_patient_record,
    register,
    register_doctor,
    register_hospital,
    register_clinic,
    register_hospital_admin,
    patient_record_lookup,
    doctor_dashboard,
    admin_dashboard,
    hospital_admin_dashboard
)
from .views import patient_record_lookup

urlpatterns = [
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('hospital-admin-login/', views.hospital_admin_login, name='hospital_admin_login'),
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<str:mr_number>/', views.patient_detail, name='patient_detail'),
    path('patients/<str:mr_number>/add-record/', views.add_patient_record, name='add_patient_record'),
    path('register/', views.register, name='register'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('register/hospital/', views.register_hospital, name='register_hospital'),
    path('register/clinic/', views.register_clinic, name='register_clinic'),
    path('register/hospital-admin/', views.register_hospital_admin, name='register_admin'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('hospital-admin/dashboard/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('patient-records/', patient_record_lookup, name='patient_record_lookup'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    # Login/logout URLs are handled in health_system/urls.py
]