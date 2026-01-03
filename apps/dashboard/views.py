from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_required
from .services import get_dashboard_stats
from attendance.models import Attendance
from leave.models import LeaveRequest
from payroll.models import Payroll


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return admin_dashboard(request)
    return employee_dashboard(request)


@login_required
def employee_dashboard(request):
    last_checkin = Attendance.objects.filter(employee=request.user).order_by('-date', '-check_in').first()
    pending_leaves = LeaveRequest.objects.filter(employee=request.user, status='pending').count()
    recent_payroll = Payroll.objects.filter(employee=request.user).order_by('-year', '-month').first()
    context = {
        'last_checkin': last_checkin,
        'pending_leaves': pending_leaves,
        'recent_payroll': recent_payroll,
    }
    return render(request, 'dashboard/employee_dashboard.html', context)


@admin_required
def admin_dashboard(request):
    stats = get_dashboard_stats()
    employees = User.objects.filter(role='employee')
    attendances = Attendance.objects.all().order_by('-date')[:10]  # recent 10
    leaves = LeaveRequest.objects.all().order_by('-requested_at')[:10]  # recent 10
    context = {
        'total_employees': stats['total_employees'],
        'pending_leaves': stats['pending_leaves'],
        'todays_attendance': stats['todays_attendance'],
        'employees': employees,
        'attendances': attendances,
        'leaves': leaves,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)