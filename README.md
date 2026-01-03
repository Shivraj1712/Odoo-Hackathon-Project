# DayFlow - HR Management System

A Django-based HR management system with multiple apps for managing employees, attendance, leave, payroll, and more.

## Features

- User authentication with role-based access (Employee, Admin)
- Email verification with OTP during registration
- Employee profiles and document management
- Attendance tracking (check-in/check-out)
- Leave request system with approval workflow
- Payroll management
- Dashboard for employees and admins with statistics
- Reports (optional)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## Usage

- Access admin at `/admin/`
- Employee dashboard at `/dashboard/`
- Admin dashboard at `/dashboard/admin/`
- Register new users and verify email with OTP

## Apps

- **accounts**: Authentication, roles, and email verification
- **dashboard**: Employee and admin dashboards with stats
- **employees**: Profiles and documents
- **attendance**: Check-in/check-out with auto time calculation
- **leave**: Leave requests with admin approval
- **payroll**: Salary management
- **reports**: Optional reports

## Email Configuration

For production, configure SMTP in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

- Jil Vaghasia (Team Leader)
- Nikunj Sorathiya
- Sanchay Singh 
- Shivrajsinh Maharaul 


### Folder Structure
    dayflow/
    │
    ├── manage.py
    │
    ├── dayflow/                     
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── apps/
    │   ├── accounts/                
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py            
    │   │   ├── forms.py             
    │   │   ├── views.py             
    │   │   ├── urls.py
    │   │   └── decorators.py        
    │   │
    │   ├── dashboard/               
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── apps.py
    │   │   ├── views.py             
    │   │   ├── urls.py
    │   │   └── services.py          
    │   │
    │   ├── employees/               
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py            
    │   │   ├── forms.py
    │   │   ├── views.py
    │   │   └── urls.py
    │   │
    │   ├── attendance/              
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py            
    │   │   ├── views.py
    │   │   ├── services.py          
    │   │   └── urls.py
    │   │
    │   ├── leave/                   
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py            
    │   │   ├── forms.py
    │   │   ├── views.py
    │   │   └── urls.py
    │   │
    │   ├── payroll/                 
    │   │   ├── migrations/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py            
    │   │   ├── views.py
    │   │   └── urls.py
    │   │
    │   └── reports/                 
    │       ├── migrations/
    │       ├── __init__.py
    │       ├── apps.py
    │       ├── views.py
    │       └── urls.py
    │
    ├── templates/
    │   ├── base.html
    │   │
    │   ├── accounts/
    │   │   ├── login.html
    │   │   └── register.html
    │   │
    │   ├── dashboard/
    │   │   ├── employee_dashboard.html
    │   │   └── admin_dashboard.html
    │   │
    │   ├── employees/
    │   │   ├── profile.html
    │   │   └── edit_profile.html
    │   │
    │   ├── attendance/
    │   │   └── attendance_list.html
    │   │
    │   ├── leave/
    │   │   ├── apply_leave.html
    │   │   └── leave_list.html
    │   │
    │   ├── payroll/
    │   │   └── payroll_view.html
    │   │
    │   └── reports/
    │       └── reports.html
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   │
    │   ├── js/
    │   │   └── main.js
    │   │
    │   └── images/
    │
    ├── media/
    │   ├── profile_pics/
    │   └── documents/
    │
    ├── requirements.txt
    └── README.md
>>>>>>> b9c214b0cc7dae47754787d2704a2ffd142f0b88
