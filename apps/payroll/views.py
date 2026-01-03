from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payroll


@login_required
def payroll_view(request):
    if request.user.role == 'admin':
        payrolls = Payroll.objects.all().order_by('-year', '-month')
    else:
        payrolls = Payroll.objects.filter(employee=request.user).order_by('-year', '-month')
    return render(request, 'payroll/payroll_view.html', {'payrolls': payrolls})