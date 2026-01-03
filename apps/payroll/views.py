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
    """Employee view - read-only payroll data showing Total Paid and Upcoming Payment"""
    payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
    
    # Calculate Total Paid (sum of all amount_paid across all payrolls)
    total_paid = sum(p.amount_paid for p in payrolls)
    
    # Calculate Upcoming Payment (sum of amount_remaining for pending/partial payrolls)
    # This includes future payrolls and unpaid portions of current payrolls
    upcoming_payment = sum(p.amount_remaining for p in payrolls if p.payment_status in ['pending', 'partial'])
    
    # Get payment history for each payroll
    payroll_list = []
    for payroll in payrolls:
        payments = Payment.objects.filter(payroll=payroll).order_by('-payment_date')
        payroll_list.append((payroll, payments))
    
    context = {
        'payroll_list': payroll_list,
        'payrolls': payrolls,
        'total_paid': total_paid,  # Total Paid
        'upcoming_payment': upcoming_payment,  # Upcoming Payment
        'total_credited': total_paid,  # Keep for backward compatibility
        'total_remaining_employee': upcoming_payment,  # Keep for backward compatibility
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
    payroll_list = []
    for payroll in payrolls:
        payments = Payment.objects.filter(payroll=payroll).order_by('-payment_date')
        payroll_list.append((payroll, payments))
    
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
def create_payroll(request):
    """Create a new payroll record for an employee (Admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('payroll_view')
    
    if request.method == 'POST':
        try:
            employee_id = int(request.POST.get('employee'))
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))
            basic_salary = float(request.POST.get('basic_salary', 0))
            allowances = float(request.POST.get('allowances', 0))
            deductions = float(request.POST.get('deductions', 0))
            working_days = int(request.POST.get('working_days', 0))
            
            employee = get_object_or_404(User, id=employee_id, role='employee')
            
            if basic_salary < 0 or allowances < 0 or deductions < 0:
                messages.error(request, 'Amounts cannot be negative.')
                return redirect('payroll_view')
            
            if working_days < 0:
                messages.error(request, 'Working days cannot be negative.')
                return redirect('payroll_view')
            
            # Check if payroll already exists for this employee/month/year
            if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
                messages.error(request, f'Payroll already exists for {employee.get_full_name() or employee.username} for {month}/{year}.')
                return redirect('payroll_view')
            
            # Create payroll
            payroll = Payroll.objects.create(
                employee=employee,
                month=month,
                year=year,
                basic_salary=basic_salary,
                allowances=allowances,
                deductions=deductions,
                working_days=working_days
            )
            
            messages.success(request, f'Payroll created successfully for {employee.get_full_name() or employee.username} - ${payroll.net_salary:.2f}')
        except ValueError:
            messages.error(request, 'Invalid input format. Please enter valid numbers.')
        except Exception as e:
            messages.error(request, f'Error creating payroll: {str(e)}')
    
    return redirect('payroll_view')


@login_required
def edit_payroll(request, payroll_id):
    """Edit payroll details - allows direct editing of payroll amount (net salary) or components (Admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('payroll_view')
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    if request.method == 'POST':
        try:
            # Check if admin wants to edit net_salary directly or use components
            edit_mode = request.POST.get('edit_mode', 'components')  # 'direct' or 'components'
            
            if edit_mode == 'direct':
                # Direct edit of net salary (payroll amount)
                net_salary = float(request.POST.get('net_salary', 0))
                working_days = int(request.POST.get('working_days', payroll.working_days))
                
                if net_salary < 0:
                    messages.error(request, 'Payroll amount cannot be negative.')
                    return redirect('payroll_view')
                
                if working_days < 0:
                    messages.error(request, 'Working days cannot be negative.')
                    return redirect('payroll_view')
                
                # Adjust basic_salary to achieve the desired net_salary
                # Formula: net_salary = basic_salary + allowances - deductions
                # Therefore: basic_salary = net_salary - allowances + deductions
                payroll.basic_salary = net_salary - payroll.allowances + payroll.deductions
                
                # Ensure basic_salary is not negative
                if payroll.basic_salary < 0:
                    # If basic_salary would be negative, adjust allowances/deductions
                    # Set basic_salary to 0 and adjust allowances
                    payroll.allowances = net_salary + payroll.deductions
                    payroll.basic_salary = 0
                
                payroll.working_days = working_days
                # Save - net_salary will be auto-calculated and should match our desired value
                payroll.save()
                
                # Verify net_salary matches (with small tolerance for floating point)
                if abs(payroll.net_salary - net_salary) > 0.01:
                    # Fine-tune to ensure exact match
                    difference = net_salary - payroll.net_salary
                    payroll.basic_salary += difference
                    payroll.save()
                
            else:
                # Edit using components (basic_salary, allowances, deductions)
                basic_salary = float(request.POST.get('basic_salary', 0))
                allowances = float(request.POST.get('allowances', 0))
                deductions = float(request.POST.get('deductions', 0))
                working_days = int(request.POST.get('working_days', payroll.working_days))
                
                if basic_salary < 0 or allowances < 0 or deductions < 0:
                    messages.error(request, 'Amounts cannot be negative.')
                    return redirect('payroll_view')
                
                if working_days < 0:
                    messages.error(request, 'Working days cannot be negative.')
                    return redirect('payroll_view')
                
                # Update payroll fields
                payroll.basic_salary = basic_salary
                payroll.allowances = allowances
                payroll.deductions = deductions
                payroll.working_days = working_days
                # net_salary will be auto-calculated in save() method
            
            # If amount_paid exceeds new net_salary, adjust it
            if payroll.amount_paid > payroll.net_salary:
                payroll.amount_paid = payroll.net_salary
                payroll.save()
            
            messages.success(request, f'Payroll amount updated successfully for {payroll.employee.get_full_name() or payroll.employee.username}. New amount: ${payroll.net_salary:.2f}')
        except ValueError:
            messages.error(request, 'Invalid input format. Please enter valid numbers.')
        except Exception as e:
            messages.error(request, f'Error updating payroll: {str(e)}')
    
    return redirect('payroll_view')


@login_required
def update_amount_paid_pending(request, payroll_id):
    """Directly update Amount Paid and Amount Pending for a specific employee (Admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('payroll_view')
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    if request.method == 'POST':
        try:
            amount_paid = float(request.POST.get('amount_paid', 0))
            amount_pending = float(request.POST.get('amount_pending', 0))
            payment_date = request.POST.get('payment_date', '')
            notes = request.POST.get('notes', '')
            
            if amount_paid < 0:
                messages.error(request, 'Amount Paid cannot be negative.')
                return redirect('payroll_view')
            
            if amount_pending < 0:
                messages.error(request, 'Amount Pending cannot be negative.')
                return redirect('payroll_view')
            
            # Validate that amount_paid + amount_pending = net_salary
            if abs((amount_paid + amount_pending) - payroll.net_salary) > 0.01:
                messages.error(request, f'Amount Paid + Amount Pending must equal Net Salary (${payroll.net_salary:.2f})')
                return redirect('payroll_view')
            
            # Calculate the difference to record as a payment transaction
            old_amount_paid = payroll.amount_paid
            payment_difference = amount_paid - old_amount_paid
            
            # Update payroll
            payroll.amount_paid = amount_paid
            if payment_date:
                payroll.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            else:
                payroll.payment_date = date.today()
            
            payroll.save()
            
            # Create payment record if there's a change
            from .models import Payment
            if abs(payment_difference) > 0.01:
                Payment.objects.create(
                    payroll=payroll,
                    amount=abs(payment_difference),
                    payment_date=payroll.payment_date,
                    notes=notes or f'Updated: Amount Paid set to ${amount_paid:.2f}, Amount Pending: ${amount_pending:.2f}',
                    created_by=request.user
                )
            
            messages.success(request, f'Payment updated for {payroll.employee.get_full_name() or payroll.employee.username}: Paid=${amount_paid:.2f}, Pending=${amount_pending:.2f}')
        except ValueError:
            messages.error(request, 'Invalid amount or date format.')
        except Exception as e:
            messages.error(request, f'Error updating payment: {str(e)}')
    
    return redirect('payroll_view')


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
            
            messages.success(request, f'Payment of ${payment_amount_to_record:.2f} recorded for {payroll.employee.get_full_name() or payroll.employee.username}')
        except ValueError:
            messages.error(request, 'Invalid amount or date format.')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
    
    return redirect('payroll_view')