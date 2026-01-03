from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:employee_id>/', views.profile, name='employee_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('list/', views.employee_list, name='employee_list'),
]