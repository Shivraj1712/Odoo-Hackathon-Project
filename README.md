# Odoo-Hackathon-Project


### Tech Stack 

- Django + Bootstramp + Vanilla JS 

---

### Team Members :

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