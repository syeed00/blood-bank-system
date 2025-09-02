from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, BloodRequest, DonationHistory

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # User will be activated after email verification
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'blood_group', 'date_of_birth', 'address', 'last_donation_date', 'is_available']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'location', 'units_required', 'urgency', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class DonationHistoryForm(forms.ModelForm):
    class Meta:
        model = DonationHistory
        fields = ['donation_date', 'units_donated', 'status', 'notes']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }