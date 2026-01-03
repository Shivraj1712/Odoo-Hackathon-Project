from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, date, timedelta
from calendar import monthrange
from .models import Payroll, Payment
from attendance.models import Attendance

User = get_user_model()


def calculate_working_days(employee, month, year):
    """Calculate working days from attendance records for a given month/year"""
    try:
        # Get first and last day of the month
        first_day = date(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = date(year, month, last_day_num)
        
        # Count present and half-day attendances
        attendances = Attendance.objects.filter(
            employee=employee,
            date__gte=first_day,
            date__lte=last_day
        )
        
        present_days = attendances.filter(status='present').count()
        half_days = attendances.filter(status='half_day').count()
        
        # Half day counts as 0.5 working days
        working_days = present_days + (half_days * 0.5)
        return int(working_days) if working_days % 1 == 0 else working_days
    except:
        return 0


@login_required
def payroll_view(request):
    if request.user.role == 'admin':
        return admin_payroll_view(request)
    else:
        return employee_payroll_view(request)


@login_required
def employee_payroll_view(request):
    """Employee view - read-only payroll data"""
    payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
    
    # Calculate totals for display
    total_to_be_credited = sum(p.net_salary for p in payrolls if p.payment_status != 'paid')
    total_credited = sum(p.amount_paid for p in payrolls)
    total_remaining_employee = sum(p.amount_remaining for p in payrolls)
    
    # Get payment history for each payroll
    payroll_list = []
    for payroll in payrolls:
        payments = Payment.objects.filter(payroll=payroll).order_by('-payment_date')
        payroll_list.append((payroll, payments))
    
    context = {
        'payroll_list': payroll_list,
        'payrolls': payrolls,
        'total_to_be_credited': total_to_be_credited,
        'total_credited': total_credited,
        'total_remaining_employee': total_remaining_employee,
    }
    return render(request, 'payroll/employee_payroll.html', context)


@login_required
def admin_payroll_view(request):
    """Admin view - comprehensive payroll management"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('payroll_view')
    
    # Get all payrolls
    payrolls = Payroll.objects.all().order_by('-year', '-month')
    
    # Statistics
    total_employees = User.objects.filter(role='employee').count()
    payroll_processed = Payroll.objects.values('month', 'year').distinct().count()
    
    # Calculate attendance stats
    today = date.today()
    current_month_start = date(today.year, today.month, 1)
    current_month_attendance = Attendance.objects.filter(
        date__gte=current_month_start,
        date__lte=today
    ).count()
    
    # Payment statistics
    total_to_be_paid = Payroll.objects.aggregate(
        total=Sum('net_salary')
    )['total'] or 0
    
    total_paid = Payroll.objects.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0
    
    total_remaining = total_to_be_paid - total_paid
    
    # Employees with pending payments
    pending_payrolls = Payroll.objects.filter(
        Q(payment_status='pending') | Q(payment_status='partial')
    ).select_related('employee')
    
    # Get current month/year from request or use current
    try:
        current_month = int(request.GET.get('month', today.month))
        current_year = int(request.GET.get('year', today.year))
    except (ValueError, TypeError):
        current_month = today.month
        current_year = today.year
    
    
    # Filter payrolls by selected month/year if specified
    if request.GET.get('month') or request.GET.get('year'):
        payrolls = payrolls.filter(month=current_month, year=current_year)
    
    # Calculate working days for each payroll if not already set
    for payroll in payrolls:
        if payroll.working_days == 0:
            payroll.working_days = calculate_working_days(
                payroll.employee, payroll.month, payroll.year
            )
            payroll.save(update_fields=['working_days'])
    
    # Get payment summaries for each payroll
    payroll_payments = {}
    for payroll in payrolls:
        payments = Payment.objects.filter(payroll=payroll).order_by('-payment_date')
        payroll_payments[payroll.id] = payments
    
    context = {
        'payroll_list': payroll_list,
        'payrolls': payrolls,
        'total_employees': total_employees,
        'payroll_processed': payroll_processed,
        'current_month_attendance': current_month_attendance,
        'total_to_be_paid': total_to_be_paid,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
        'pending_payrolls': pending_payrolls,
        'current_month': current_month,
        'current_year': current_year,
        'today': today,
    }
    return render(request, 'payroll/admin_payroll.html', context)


@login_required
def update_payment(request, payroll_id):
    """Update payment amount and status (Admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('payroll_view')
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'incremental')  # incremental or total
        payment_amount = request.POST.get('payment_amount')
        payment_date = request.POST.get('payment_date')
        notes = request.POST.get('notes', '')
        
        try:
            amount = float(payment_amount)
            
            if amount <= 0:
                messages.error(request, 'Payment amount must be greater than zero.')
                return redirect('payroll_view')
            
            # Store old amount for payment record
            old_amount_paid = payroll.amount_paid
            payment_amount_to_record = 0
            
            if payment_type == 'incremental':
                # Add to existing amount
                if amount > payroll.amount_remaining:
                    messages.error(request, f'Payment exceeds remaining amount. Maximum: ${payroll.amount_remaining:.2f}')
                    return redirect('payroll_view')
                payroll.amount_paid = payroll.amount_paid + amount
                payment_amount_to_record = amount
            else:
                # Set total amount
                if amount > payroll.net_salary:
                    messages.error(request, f'Payment cannot exceed net salary of ${payroll.net_salary:.2f}')
                    return redirect('payroll_view')
                if amount < old_amount_paid:
                    messages.error(request, f'New total cannot be less than current amount paid (${old_amount_paid:.2f})')
                    return redirect('payroll_view')
                payment_amount_to_record = amount - old_amount_paid
                payroll.amount_paid = amount
            
            if payment_date:
                payroll.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            else:
                payroll.payment_date = date.today()
            
            payroll.save()
            
            # Create payment record
            from .models import Payment
            if payment_amount_to_record > 0:
                Payment.objects.create(
                    payroll=payroll,
                    amount=payment_amount_to_record,
                    payment_date=payroll.payment_date,
                    notes=notes,
                    created_by=request.user
                )
            
            messages.success(request, f'Payment of ${amount:.2f} recorded for {payroll.employee.get_full_name() or payroll.employee.username}')
        except ValueError:
            messages.error(request, 'Invalid amount or date format.')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
    
    return redirect('payroll_view')