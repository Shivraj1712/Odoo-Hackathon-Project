from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.accounts.decorators import admin_required
from .models import LeaveRequest
from .forms import LeaveRequestForm, LeaveApprovalForm


@login_required
def leave_list(request):
    if request.user.role == 'admin':
        leaves = LeaveRequest.objects.all().order_by('-requested_at')
    else:
        leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-requested_at')
    return render(request, 'leave/leave_list.html', {'leaves': leaves})


@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, 'Leave request submitted successfully. Waiting for approval.')
            return redirect('leave_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave/apply_leave.html', {'form': form})


@admin_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('admin_comments', '')
        
        if action == 'approve':
            leave.approve(request.user, comments)
            messages.success(request, f'Leave request from {leave.employee.get_full_name() or leave.employee.username} has been approved.')
        elif action == 'reject':
            leave.reject(request.user, comments)
            messages.success(request, f'Leave request from {leave.employee.get_full_name() or leave.employee.username} has been rejected.')
        return redirect('leave_list')
    
    # GET request - show approval form
    form = LeaveApprovalForm(instance=leave)
    return render(request, 'leave/approve_leave.html', {'leave': leave, 'form': form})