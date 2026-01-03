from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_view, name='payroll_view'),
    path('create/', views.create_payroll, name='create_payroll'),
    path('bulk-create/', views.bulk_create_payrolls, name='bulk_payroll'),
    path('edit/<int:payroll_id>/', views.edit_payroll, name='edit_payroll'),
    path('update-amount/<int:payroll_id>/', views.update_amount_paid_pending, name='update_amount_paid_pending'),
    path('update-payment/<int:payroll_id>/', views.update_payment, name='update_payment'),
]