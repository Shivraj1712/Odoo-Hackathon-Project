from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_required
from .services import get_dashboard_stats


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return admin_dashboard(request)
    return employee_dashboard(request)


@login_required
def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html')


@admin_required
def admin_dashboard(request):
    stats = get_dashboard_stats()
    return render(request, 'dashboard/admin_dashboard.html', stats)