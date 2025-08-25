from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django import forms
from .models import Hospital, Patient, Doctor, PatientRecord, Clinic, HospitalAdmin as HospitalAdminModel

class CustomAdminSite(admin.AdminSite):
    site_header = 'Health Management System'
    site_title = 'Admin Dashboard'
    index_title = 'Dashboard'

    def has_permission(self, request):
        # Allow access to superusers and staff members
        if request.user.is_superuser or request.user.is_staff:
            return True
        # Allow access to hospital users for their specific sections
        if hasattr(request.user, 'hospital') and request.user.is_authenticated:
            return True
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.admin_dashboard), name='dashboard'),
        ]
        return custom_urls + urls
    
    def admin_dashboard(self, request):
        if not request.user.is_staff:
            return redirect('admin:login')
            
        context = {
            'patient_count': Patient.objects.count(),
            'doctor_count': Doctor.objects.count(),
            'hospital_count': Hospital.objects.count(),
            'record_count': PatientRecord.objects.count(),
            **self.each_context(request),
            'title': 'Admin Dashboard',
            'opts': self._registry.keys(),
        }
        return render(request, 'admin/custom_dashboard.html', context)

# Create instance and register models
custom_admin_site = CustomAdminSite(name='custom_admin')

class HospitalAdminForm(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Hospital
        fields = '__all__'

class HospitalAdmin(admin.ModelAdmin):
    form = HospitalAdminForm
    list_display = ('name', 'get_username', 'registration_number', 'hospital_type', 'city', 'contact_person_name')
    list_filter = ('hospital_type', 'city', 'state')
    search_fields = ('name', 'registration_number', 'contact_person_name', 'email', 'user__username')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Hospital Information', {
                'fields': ('name', 'registration_number', 'hospital_type')
            }),
            ('Address', {
                'fields': ('street_address', 'city', 'state', 'postal_code', 'country')
            }),
            ('Contact Information', {
                'fields': ('contact_person_name', 'designation', 'contact_number', 'email', 'alternate_contact', 'fax_number')
            })
        ]
        
        # Only add user account fields if the user has sufficient permissions
        if request.user.is_superuser or request.user.is_staff:
            fieldsets.insert(1, ('User Account', {
                'fields': ('username', 'password'),
                'description': 'Create or update user account for hospital login'
            }))
        
        return fieldsets

    def get_username(self, obj):
        return obj.user.username if obj.user else '-'
    get_username.short_description = 'Username'

    def save_model(self, request, obj, form, change):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        if username:
            if not obj.user:
                # Create new user
                user = User.objects.create_user(username=username, password=password)
                obj.user = user
            else:
                # Update existing user
                obj.user.username = username
                if password:
                    obj.user.set_password(password)
                obj.user.save()

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.user:
            form.base_fields['username'].initial = obj.user.username
        return form

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated

# Register all models with the custom admin site
custom_admin_site.register(Patient)
custom_admin_site.register(Doctor)
custom_admin_site.register(Hospital, HospitalAdmin)
custom_admin_site.register(PatientRecord)
custom_admin_site.register(HospitalAdminModel)
custom_admin_site.register(Clinic)