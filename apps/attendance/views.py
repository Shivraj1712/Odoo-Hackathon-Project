from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import Attendance


@login_required
def attendance_list(request):
    attendances = Attendance.objects.filter(employee=request.user).order_by('-date')
    today = date.today()
    try:
        today_attendance = Attendance.objects.get(employee=request.user, date=today)
        checked_in = today_attendance.check_in is not None
    except Attendance.DoesNotExist:
        checked_in = False
    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances,
        'checked_in': checked_in,
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