from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, date

User = get_user_model()


class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')

    def save(self, *args, **kwargs):
        if self.check_in and self.check_out:
            dummy_date = date.today()
            check_in_dt = datetime.combine(dummy_date, self.check_in)
            check_out_dt = datetime.combine(dummy_date, self.check_out)
            if check_out_dt > check_in_dt:
                duration = check_out_dt - check_in_dt
                self.hours_worked = round(duration.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"