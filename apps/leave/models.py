from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    LEAVE_TYPE_CHOICES = [
        ('paid', 'Paid Leave'),
        ('sick', 'Sick Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES, default='paid')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    admin_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date}"
    
    def approve(self, admin_user, comments=''):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.approved_by = admin_user
        self.admin_comments = comments
        self.save()
    
    def reject(self, admin_user, comments=''):
        self.status = 'rejected'
        self.approved_at = timezone.now()
        self.approved_by = admin_user
        self.admin_comments = comments
        self.save()