from django import forms
from django.contrib.auth import get_user_model
from .models import EmployeeProfile

User = get_user_model()


class EmployeeProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
        label='Last Name'
    )
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Update User model fields
            if instance and instance.user:
                instance.user.first_name = self.cleaned_data.get('first_name', '')
                instance.user.last_name = self.cleaned_data.get('last_name', '')
                instance.user.save()
        return instance