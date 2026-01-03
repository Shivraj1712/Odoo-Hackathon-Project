from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import Attendance
from accounts.models import User
from apps.accounts.decorators import admin_required


@login_required
def attendance_list(request):
    employee_id = request.GET.get('employee_id')
    
    # Admin can view all attendance or filter by employee
    if request.user.role == 'admin':
        if employee_id:
            employee = get_object_or_404(User, id=employee_id)
            attendances = Attendance.objects.filter(employee=employee).order_by('-date')
            selected_employee = employee
        else:
            attendances = Attendance.objects.all().order_by('-date')
            selected_employee = None
        checked_in = None  # Admin doesn't need check-in button
    else:
        attendances = Attendance.objects.filter(employee=request.user).order_by('-date')
        selected_employee = None
        today = date.today()
        try:
            today_attendance = Attendance.objects.get(employee=request.user, date=today)
            checked_in = today_attendance.check_in is not None
        except Attendance.DoesNotExist:
            checked_in = False
    
    # Get all employees for admin filter dropdown
    employees = User.objects.filter(role='employee') if request.user.role == 'admin' else None
    
    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'checked_in': checked_in,
        'employees': employees,
        'selected_employee': selected_employee,
    })


@login_required
def check_in(request):
    if request.method == 'POST':
        today = date.today()
        attendance, created = Attendance.objects.get_or_create(
            employee=request.user,
            date=today,
            defaults={'check_in': timezone.now().time()}
        )
        if not created and not attendance.check_in:
            attendance.check_in = timezone.now().time()
            attendance.save()
        messages.success(request, 'Checked in successfully.')
    return redirect('attendance_list')


@login_required
def check_out(request):
    if request.method == 'POST':
        today = date.today()
        try:
            attendance = Attendance.objects.get(employee=request.user, date=today)
            if not attendance.check_out:
                attendance.check_out = timezone.now().time()
                attendance.save()
                messages.success(request, 'Checked out successfully.')
            else:
                messages.warning(request, 'Already checked out.')
        except Attendance.DoesNotExist:
            messages.error(request, 'No check-in record found for today.')
    return redirect('attendance_list')