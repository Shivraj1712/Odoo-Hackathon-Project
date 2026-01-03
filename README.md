# DayFlow - HR Management System

A Django-based HR management system with multiple apps for managing employees, attendance, leave, payroll, and more.

## Features

- User authentication with role-based access (Employee, Admin)
- Employee profiles and document management
- Attendance tracking (check-in/check-out)
- Leave request system
- Payroll management
- Dashboard for employees and admins
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

## Apps

- **accounts**: Authentication and roles
- **dashboard**: Employee and admin dashboards
- **employees**: Profiles and documents
- **attendance**: Check-in/check-out
- **leave**: Leave requests
- **payroll**: Salary management
- **reports**: Optional reports