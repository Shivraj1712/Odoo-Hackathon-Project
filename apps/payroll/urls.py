from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_view, name='payroll_view'),
    path('update-payment/<int:payroll_id>/', views.update_payment, name='update_payment'),
]