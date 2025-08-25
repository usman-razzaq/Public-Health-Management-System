from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.admin_dashboard), name='admin_dashboard'),
        ]
        return custom_urls + urls
    
    @staff_member_required
    def admin_dashboard(self, request):
        from .models import Patient, Doctor, Hospital, PatientRecord  # Import here to avoid circular imports
        context = {
            'patient_count': Patient.objects.count(),
            'doctor_count': Doctor.objects.count(),
            'hospital_count': Hospital.objects.count(),
            'record_count': PatientRecord.objects.count(),
            **self.each_context(request),
            'title': 'Admin Dashboard',
        }
        return render(request, 'admin/custom_dashboard.html', context)

# Then register models after class definition
custom_admin_site = CustomAdminSite(name='custom_admin')

# Lazy import models for registration
def register_models():
    from .models import Patient, Doctor, Hospital, PatientRecord
    custom_admin_site.register(Patient)
    custom_admin_site.register(Doctor)
    custom_admin_site.register(Hospital)
    custom_admin_site.register(PatientRecord)

register_models()