from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, date

User = get_user_model()


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half-day'),
        ('leave', 'Leave'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    class Meta:
        unique_together = ('employee', 'date')
        verbose_name_plural = 'Attendances'

    def save(self, *args, **kwargs):
        # Auto-determine status based on check-in/check-out
        if self.check_in and self.check_out:
            dummy_date = date.today()
            check_in_dt = datetime.combine(dummy_date, self.check_in)
            check_out_dt = datetime.combine(dummy_date, self.check_out)
            if check_out_dt > check_in_dt:
                duration = check_out_dt - check_in_dt
                hours = duration.total_seconds() / 3600
                self.hours_worked = round(hours, 2)
                # If worked less than 4 hours, consider it half-day
                if hours < 4:
                    self.status = 'half_day'
                else:
                    self.status = 'present'
        elif self.check_in and not self.check_out:
            self.status = 'present'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.date} ({self.get_status_display()})"