from accounts.models import User
from leave.models import LeaveRequest
from attendance.models import Attendance
from datetime import date


def get_dashboard_stats():
    total_employees = User.objects.filter(role='employee').count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    todays_attendance = Attendance.objects.filter(date=date.today()).count()
    return {
        'total_employees': total_employees,
        'pending_leaves': pending_leaves,
        'todays_attendance': todays_attendance,
    }