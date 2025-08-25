from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Patient, Doctor, Clinic, Hospital, PatientRecord, HospitalAdmin

class PatientForm(forms.ModelForm):
    mr_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter MR number (min 5 characters)'}))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    blood_group = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blood group'}))
    address = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter complete address'}))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    registered_at = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Patient
        fields = ['mr_number', 'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group', 'address', 'contact_number', 'email', 'registered_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registered_at'].empty_label = "Select Hospital"

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user']

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = '__all__'

class HospitalForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    
    class Meta:
        model = Hospital
        fields = ['username', 'password', 'confirm_password', 'name', 'registration_number', 'hospital_type', 'street_address', 'city', 'state', 'postal_code', 'country', 'contact_person_name', 'designation', 'contact_number', 'email', 'alternate_contact', 'fax_number']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
            
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        
        return cleaned_data
        
    def save(self, commit=True):
        hospital = super().save(commit=False)
        
        # Create user account
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        
        hospital.user = user
        if commit:
            hospital.save()
        return hospital

class HospitalAdminForm(forms.ModelForm):
    class Meta:
        model = HospitalAdmin
        exclude = ['user']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.all()
        self.fields['hospital'].empty_label = "Select Hospital"

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['symptoms', 'diagnosis', 'prescription', 'notes', 'next_visit']
        widgets = {
            'next_visit': forms.DateInput(attrs={'type': 'date'}),
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("There is no user registered with this email address.")
        return email

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        strip=False,
    )

class DoctorRegistrationForm(CustomUserCreationForm):
    specialization = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    license_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    clinic = forms.ModelChoiceField(queryset=Clinic.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('specialization', 'license_number', 'clinic')

class HospitalRegistrationForm(forms.ModelForm):
    # Hospital Information
    name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hospital name'}))
    registration_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration number (Govt. or Medical Council ID)'}))
    hospital_type = forms.ChoiceField(choices=Hospital.HOSPITAL_TYPES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Password fields
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}), required=True)
    
    # Address Information
    street_address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street address'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city/district'}))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter province/state'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    
    # Contact Information
    contact_person_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter primary contact person name'}))
    designation = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    alternate_contact = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter alternate contact number (optional)'}))
    fax_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter fax number (optional)'}))
    
    class Meta:
        model = Hospital
        fields = ('name', 'registration_number', 'hospital_type', 'street_address', 'city', 'state', 'postal_code', 'country', 
                 'contact_person_name', 'designation', 'contact_number', 'email', 'alternate_contact', 'fax_number')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class HospitalAdminRegistrationForm(CustomUserCreationForm):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('hospital', 'position', 'contact_number')

class ClinicRegistrationForm(forms.ModelForm):
    # Clinic Information
    name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter clinic name'}))
    clinic_type = forms.ChoiceField(choices=Clinic.CLINIC_TYPES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    registration_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration number (Medical Council or Govt. issued)'}))
    license_number = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter license number'}))
    establishment_year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter establishment year'}))
    # Temporarily make hospital field not required to avoid the error
    hospital_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter associated hospital name'}))
    specialization = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization'}))
    
    # Contact Information
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter clinic email address'}))
    contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter primary phone number'}))
    alternate_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter alternate phone number (optional)'}))
    whatsapp_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter official WhatsApp number (optional)'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter website URL (optional)'}))
    
    # Address Information
    street_address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street address'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city/district'}))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter province/state'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    
    # Owner/Admin Information
    owner_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter owner/administrator name'}))
    cnic_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CNIC/NIC number'}))
    designation = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation (e.g., Doctor, Manager)'}))
    owner_mobile = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    owner_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    
    # Login Credentials
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}), required=True)
    
    class Meta:
        model = Clinic
        fields = ('name', 'clinic_type', 'registration_number', 'license_number', 'establishment_year', 'specialization',
                 'email', 'contact_number', 'alternate_number', 'whatsapp_number', 'website',
                 'street_address', 'city', 'state', 'postal_code', 'country',
                 'owner_name', 'cnic_number', 'designation', 'owner_mobile', 'owner_email')
        # Exclude hospital field from the form to avoid the error
        exclude = ('hospital',)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class PatientRegistrationForm(forms.ModelForm):
    # Personal Information
    full_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    cnic_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CNIC/National ID Number'}))
    marital_status = forms.ChoiceField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    blood_group = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blood group (optional)'}))
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    # Contact Information
    mobile_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    emergency_contact_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter emergency contact name'}))
    emergency_contact_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter emergency contact number'}))
    relationship_to_emergency_contact = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter relationship to emergency contact'}))
    
    # Address Information
    street_address = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street address'}))
    city = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city/district'}))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter province/state'}))
    postal_code = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    
    # Medical Information (optional)
    known_allergies = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter known allergies (optional)'}))
    chronic_conditions = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter chronic conditions (e.g., Diabetes, Hypertension) (optional)'}))
    current_medications = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter current medications (optional)'}))
    disability_status = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Login Credentials
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}), required=True)
    
    # Hospital Registration
    registered_at = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'blood_group', 'contact_number', 'email', 'registered_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registered_at'].empty_label = "Select Hospital"
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data