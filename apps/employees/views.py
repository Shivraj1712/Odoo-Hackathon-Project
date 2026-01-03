from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmployeeProfile
from .forms import EmployeeProfileForm


@login_required
def profile(request):
    profile, created = EmployeeProfile.objects.get_or_create(user=request.user)
    return render(request, 'employees/profile.html', {'profile': profile})


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