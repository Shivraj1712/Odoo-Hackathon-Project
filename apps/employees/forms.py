from django import forms
from .models import EmployeeProfile


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['phone', 'address', 'profile_pic', 'date_of_birth', 'hire_date']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'phone': 'Phone Number',
            'address': 'Address',
            'profile_pic': 'Profile Picture',
            'date_of_birth': 'Date of Birth',
            'hire_date': 'Hire Date',
        }