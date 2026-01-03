from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_required


@admin_required
def reports(request):
    return render(request, 'reports/reports.html')