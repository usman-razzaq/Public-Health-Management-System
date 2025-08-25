from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Patient, Doctor, Clinic, Hospital, PatientRecord, HospitalAdmin
from .forms import (
    PatientForm, DoctorForm, ClinicForm, HospitalForm, PatientRecordForm, 
    CustomUserCreationForm, DoctorRegistrationForm, HospitalRegistrationForm,
    ClinicRegistrationForm, HospitalAdminRegistrationForm, PatientRegistrationForm
)
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if not username or not password:
            return render(request, 'registration/login.html', {'error': 'Please enter both username and password'})

        if not user_type:
            return render(request, 'registration/login.html', {'error': 'Invalid login attempt. Please try again.'})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                return render(request, 'registration/login.html', {'error': 'Your account is disabled. Please contact the administrator.'})

            if user_type == 'doctor':
                if hasattr(user, 'doctor'):
                    login(request, user)
                    return redirect('doctor_dashboard')
                else:
                    return render(request, 'registration/login.html', {'error': 'This account does not have doctor privileges'})
            
            elif user_type == 'hospital_admin':
                if hasattr(user, 'hospitaladmin'):
                    login(request, user)
                    return redirect('hospital_admin_dashboard')
                else:
                    return render(request, 'registration/login.html', {'error': 'This account does not have hospital admin privileges'})
            
            elif user_type == 'admin':
                if user.is_staff:
                    login(request, user)
                    return redirect('admin_dashboard')
                else:
                    return render(request, 'registration/login.html', {'error': 'This account does not have admin privileges'})
            
            else:
                return render(request, 'registration/login.html', {'error': 'Invalid user type selected'})
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid username or password'})
    
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            return redirect('doctor_dashboard')
        elif hasattr(request.user, 'hospitaladmin'):
            return redirect('hospital_admin_dashboard')
        elif request.user.is_staff:
            return redirect('admin_dashboard')
    
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'doctor'):
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid doctor credentials'
            })
    return redirect('login')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid admin credentials'
            })
    return redirect('login')

def hospital_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'hospitaladmin'):
            login(request, user)
            return redirect('hospital_admin_dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid hospital admin credentials'
            })
    return redirect('login')

def root_redirect(request):
    # Always redirect to login page, regardless of authentication status
    return redirect('login')

def patient_record_lookup(request):
    if request.method == 'GET' and 'mr_number' in request.GET:
        mr_number = request.GET.get('mr_number')
        try:
            patient = Patient.objects.get(mr_number=mr_number)
            records = PatientRecord.objects.filter(patient=patient).order_by('-visit_date')
            return render(request, 'core/patient_records.html', {
                'patient': patient,
                'records': records
            })
        except Patient.DoesNotExist:
            return render(request, 'registration/login.html', {
                'error': 'No records found for the provided MR number'
            })
    return redirect('login')

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('login')
    
    # Get doctor's patients and recent records
    doctor = request.user.doctor
    patients = Patient.objects.filter(patientrecord__doctor=doctor).distinct()
    recent_records = PatientRecord.objects.filter(doctor=doctor).order_by('-visit_date')[:10]
    
    return render(request, 'core/doctor_dashboard.html', {
        'patients': patients,
        'recent_records': recent_records
    })

@staff_member_required
def admin_dashboard(request):
    stats = {
        'patient_count': Patient.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'hospital_count': Hospital.objects.count(),
        'record_count': PatientRecord.objects.count(),
    }
    return render(request, 'admin/custom_dashboard.html', stats)

@login_required
def hospital_admin_dashboard(request):
    if not hasattr(request.user, 'hospitaladmin'):
        return redirect('login')
    
    # Get hospital admin's hospital and related data
    hospital_admin = request.user.hospitaladmin
    hospital = hospital_admin.hospital
    
    # Get statistics for this hospital
    stats = {
        'hospital': hospital,
        'patient_count': Patient.objects.filter(registered_at=hospital).count(),
        'doctor_count': Doctor.objects.filter(clinic__hospital=hospital).count(),
        'record_count': PatientRecord.objects.filter(patient__registered_at=hospital).count(),
        'recent_patients': Patient.objects.filter(registered_at=hospital).order_by('-registration_date')[:10],
        'recent_records': PatientRecord.objects.filter(patient__registered_at=hospital).order_by('-visit_date')[:10],
    }
    
    return render(request, 'core/hospital_admin_dashboard.html', stats)

@login_required
def dashboard(request):
    if hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    elif hasattr(request.user, 'hospitaladmin'):
        return redirect('hospital_admin_dashboard')
    elif request.user.is_staff:
        return redirect('admin_dashboard')
    
    # Regular user dashboard - show recent patients and records
    recent_patients = Patient.objects.all().order_by('-registration_date')[:5]
    recent_records = PatientRecord.objects.all().order_by('-visit_date')[:5]
    
    return render(request, 'core/dashboard.html', {
        'patients': recent_patients,
        'records': recent_records
    })

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-registration_date')
    return render(request, 'core/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, mr_number):
    patient = get_object_or_404(Patient, mr_number=mr_number)
    records = PatientRecord.objects.filter(patient=patient).order_by('-visit_date')
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'records': records
    })

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'core/add_patient.html', {'form': form})

@login_required
def add_patient_record(request, mr_number):
    patient = get_object_or_404(Patient, mr_number=mr_number)
    
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            if hasattr(request.user, 'doctor'):
                record.doctor = request.user.doctor
            record.save()
            return redirect('patient_detail', mr_number=mr_number)
    else:
        form = PatientRecordForm()
    
    return render(request, 'core/add_patient_record.html', {
        'form': form,
        'patient': patient
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Register User'})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Create the doctor profile
            doctor = Doctor.objects.create(
                user=user,
                specialization=form.cleaned_data['specialization'],
                license_number=form.cleaned_data['license_number'],
                clinic=form.cleaned_data['clinic']
            )
            
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Register Doctor'})

def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            # Create hospital but don't save password fields to the model
            hospital = form.save(commit=False)
            hospital.save()
            
            # Create a success message
            messages.success(request, 'Hospital registered successfully! You can now login.')
            return redirect('login')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Register Hospital'})

def register_clinic(request):
    if request.method == 'POST':
        form = ClinicRegistrationForm(request.POST)
        if form.is_valid():
            # Create clinic but don't save username and password fields to the model
            clinic = form.save(commit=False)
            
            # Handle the hospital relationship
            hospital_name = form.cleaned_data.get('hospital_name')
            # Try to find an existing hospital with this name, or create a default one
            try:
                hospital = Hospital.objects.filter(name__icontains=hospital_name).first()
                if not hospital:
                    # Create a temporary hospital with minimal information
                    hospital = Hospital.objects.create(
                        name=hospital_name,
                        contact_number='0000000000',  # Default value
                        email='temp@example.com'      # Default value
                    )
                clinic.hospital = hospital
            except Exception as e:
                # If there's any error with hospital, create a default one
                hospital = Hospital.objects.create(
                    name='Default Hospital',
                    contact_number='0000000000',
                    email='default@example.com'
                )
                clinic.hospital = hospital
            
            clinic.save()
            
            # Create a user account for clinic login
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            
            # Set user as staff to allow login to admin area
            user.is_staff = True
            user.save()
            
            # Create a success message
            messages.success(request, 'Clinic registered successfully! You can now login.')
            return redirect('login')
    else:
        form = ClinicRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Register Clinic'})

def register_hospital_admin(request):
    if request.method == 'POST':
        form = HospitalAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Create the hospital admin profile
            hospital_admin = HospitalAdmin.objects.create(
                user=user,
                hospital=form.cleaned_data['hospital'],
                position=form.cleaned_data['position'],
                contact_number=form.cleaned_data['contact_number']
            )
            
            login(request, user)
            return redirect('hospital_admin_dashboard')
    else:
        form = HospitalAdminRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Register Hospital Admin'})

# Additional views for managing doctors, clinics, hospitals would follow similar patterns

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new patient instance but don't save yet
            patient = form.save(commit=False)
            
            # Generate a unique MR number (you might want to implement a more sophisticated method)
            import uuid
            patient.mr_number = str(uuid.uuid4())[:8].upper()
            
            # Set the registration date
            from django.utils import timezone
            patient.registration_date = timezone.now()
            
            # Save the patient
            patient.save()
            
            # Create a success message
            messages.success(request, f'Patient registered successfully! Your Medical Record Number is {patient.mr_number}')
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': 'Patient Registration', 'user_type': 'patient'})