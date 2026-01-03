from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployeeProfile
from .forms import EmployeeProfileForm
from apps.accounts.decorators import admin_required
from accounts.models import User


@login_required
def profile(request, employee_id=None):
    # Admin can view any employee's profile
    if employee_id and request.user.role == 'admin':
        employee = get_object_or_404(User, id=employee_id)
        profile_obj, created = EmployeeProfile.objects.get_or_create(user=employee)
        is_admin_view = True
    else:
        profile_obj, created = EmployeeProfile.objects.get_or_create(user=request.user)
        is_admin_view = False
    
    return render(request, 'employees/profile.html', {
        'profile': profile_obj,
        'is_admin_view': is_admin_view,
    })


@login_required
def edit_profile(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EmployeeProfileForm(instance=profile)
    return render(request, 'employees/edit_profile.html', {'form': form})


@admin_required
def employee_list(request):
    employees = EmployeeProfile.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})