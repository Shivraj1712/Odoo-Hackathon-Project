from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Enter reason for leave...'}),
        }
        labels = {
            'leave_type': 'Leave Type',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Remarks/Reason',
        }


class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['admin_comments']
        widgets = {
            'admin_comments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Add comments (optional)...'}),
        }
        labels = {
            'admin_comments': 'Comments',
        }