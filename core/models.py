from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils import timezone

User = get_user_model()  # Use this instead of direct User import

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    HOSPITAL_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('military', 'Military'),
        ('trust', 'Trust'),
        ('ngo', 'NGO'),
    ]
    
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, default='REG-00000')  # Removed unique=True temporarily
    hospital_type = models.CharField(max_length=20, choices=HOSPITAL_TYPES, default='private')
    
    # Address fields
    street_address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    postal_code = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=100, default='')
    
    # Contact information
    contact_person_name = models.CharField(max_length=100, default='')
    designation = models.CharField(max_length=100, default='')
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    alternate_contact = models.CharField(max_length=15, blank=True, null=True)
    fax_number = models.CharField(max_length=15, blank=True, null=True)
    
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Clinic(models.Model):
    CLINIC_TYPES = [
        ('general', 'General'),
        ('dental', 'Dental'),
        ('eye', 'Eye'),
        ('physiotherapy', 'Physiotherapy'),
        ('homeopathy', 'Homeopathy'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedic', 'Orthopedic'),
        ('pediatric', 'Pediatric'),
        ('gynecology', 'Gynecology'),
        ('other', 'Other'),
    ]
    
    # Clinic Information
    name = models.CharField(max_length=200)
    clinic_type = models.CharField(max_length=20, choices=CLINIC_TYPES, default='general')
    registration_number = models.CharField(max_length=50, unique=True, default='CREG-00000')
    license_number = models.CharField(max_length=50, default='LIC-00000')
    establishment_year = models.IntegerField(null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    # Contact Information
    email = models.EmailField(default='')
    contact_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Address Information
    street_address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    postal_code = models.CharField(max_length=20, default='')
    country = models.CharField(max_length=100, default='')
    
    # Owner/Admin Information
    owner_name = models.CharField(max_length=100, default='')
    cnic_number = models.CharField(max_length=20, default='')
    designation = models.CharField(max_length=100, default='')
    owner_mobile = models.CharField(max_length=15, default='')
    owner_email = models.EmailField(default='')
    
    # Additional Information
    specialization = models.CharField(max_length=200)
    registration_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} ({self.clinic_type}) - {self.hospital.name}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Patient(models.Model):
    mr_number = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(5)])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=5, blank=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    registered_at = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (MR: {self.mr_number})"

class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    next_visit = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.visit_date}"

class HospitalAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.hospital.name} Administrator"