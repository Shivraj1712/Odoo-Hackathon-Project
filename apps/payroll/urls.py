from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_view, name='payroll_view'),
]