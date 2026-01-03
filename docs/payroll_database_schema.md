# Payroll Module - Database Schema Documentation

## Overview
This document describes the database schema for the Payroll module, including SQL table structures and JSON data representation.

---

## SQL Database Schema

### Table: `payroll_payroll`
Stores payroll information for each employee per month/year.

```sql
CREATE TABLE payroll_payroll (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_id BIGINT NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    basic_salary DECIMAL(10, 2) NOT NULL,
    allowances DECIMAL(10, 2) DEFAULT 0.00,
    deductions DECIMAL(10, 2) DEFAULT 0.00,
    net_salary DECIMAL(10, 2) NOT NULL,
    amount_paid DECIMAL(10, 2) DEFAULT 0.00,
    amount_pending DECIMAL(10, 2) GENERATED ALWAYS AS (net_salary - amount_paid) STORED,
    payment_status VARCHAR(10) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'partial')),
    payment_date DATE NULL,
    working_days INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_employee_month_year (employee_id, month, year),
    FOREIGN KEY (employee_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    INDEX idx_employee (employee_id),
    INDEX idx_month_year (year, month),
    INDEX idx_payment_status (payment_status)
);
```

**Field Descriptions:**
- `id`: Primary key
- `employee_id`: Foreign key to User table
- `month`: Month number (1-12)
- `year`: Year (e.g., 2025)
- `basic_salary`: Base salary amount
- `allowances`: Additional allowances (bonuses, incentives)
- `deductions`: Deductions (taxes, loans)
- `net_salary`: Calculated as `basic_salary + allowances - deductions`
- `amount_paid`: Total amount paid to employee
- `amount_pending`: Calculated as `net_salary - amount_paid` (virtual field)
- `payment_status`: Status of payment ('pending', 'paid', 'partial')
- `payment_date`: Date of last payment
- `working_days`: Number of working days in the period
- `created_at`: Record creation timestamp
- `updated_at`: Record last update timestamp

---

### Table: `payroll_payment`
Stores individual payment transactions for tracking payment history.

```sql
CREATE TABLE payroll_payment (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    payroll_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    notes TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by_id BIGINT NULL,
    FOREIGN KEY (payroll_id) REFERENCES payroll_payroll(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES accounts_user(id) ON DELETE SET NULL,
    INDEX idx_payroll (payroll_id),
    INDEX idx_payment_date (payment_date),
    INDEX idx_created_at (created_at)
);
```

**Field Descriptions:**
- `id`: Primary key
- `payroll_id`: Foreign key to Payroll table
- `amount`: Payment amount
- `payment_date`: Date of payment
- `notes`: Optional notes about the payment
- `created_at`: Transaction creation timestamp (includes time)
- `created_by_id`: User who recorded the payment

---

## JSON Data Structure

### Payroll Object
```json
{
    "id": 1,
    "employee": {
        "id": 5,
        "username": "john.doe",
        "email": "john.doe@example.com",
        "full_name": "John Doe"
    },
    "month": 1,
    "year": 2025,
    "basic_salary": "5000.00",
    "allowances": "500.00",
    "deductions": "200.00",
    "net_salary": "5300.00",
    "amount_paid": "3000.00",
    "amount_pending": "2300.00",
    "payment_status": "partial",
    "payment_date": "2025-01-15",
    "working_days": 22,
    "created_at": "2025-01-01T10:00:00Z",
    "updated_at": "2025-01-15T14:30:00Z"
}
```

### Payment Transaction Object
```json
{
    "id": 1,
    "payroll_id": 1,
    "amount": "1500.00",
    "payment_date": "2025-01-15",
    "notes": "First installment payment",
    "created_at": "2025-01-15T14:30:00Z",
    "created_by": {
        "id": 1,
        "username": "admin",
        "full_name": "Admin User"
    }
}
```

### Employee Payroll Summary (Employee View)
```json
{
    "total_paid": "15000.00",
    "upcoming_payment": "5300.00",
    "payrolls": [
        {
            "id": 1,
            "month": 1,
            "year": 2025,
            "net_salary": "5300.00",
            "amount_paid": "3000.00",
            "amount_pending": "2300.00",
            "payment_status": "partial",
            "payment_date": "2025-01-15"
        }
    ],
    "payment_history": [
        {
            "id": 1,
            "amount": "1500.00",
            "payment_date": "2025-01-15",
            "created_at": "2025-01-15T14:30:00Z",
            "notes": "First installment"
        }
    ]
}
```

### Admin Payroll Summary
```json
{
    "employee_id": 5,
    "employee_name": "John Doe",
    "month": 1,
    "year": 2025,
    "net_salary": "5300.00",
    "amount_paid": "3000.00",
    "amount_pending": "2300.00",
    "payment_status": "partial",
    "payment_history": [
        {
            "id": 1,
            "amount": "1500.00",
            "payment_date": "2025-01-15",
            "created_at": "2025-01-15T14:30:00Z",
            "created_by": "Admin User",
            "notes": "First installment"
        }
    ]
}
```

---

## Key Relationships

1. **Payroll → Employee**: One employee can have multiple payroll records (one per month/year)
2. **Payment → Payroll**: One payroll can have multiple payment transactions
3. **Payment → User (created_by)**: Tracks who recorded each payment

---

## Calculated Fields

### Amount Pending
```sql
amount_pending = net_salary - amount_paid
```

### Net Salary
```sql
net_salary = basic_salary + allowances - deductions
```

### Payment Status Logic
- `pending`: `amount_paid = 0`
- `partial`: `0 < amount_paid < net_salary`
- `paid`: `amount_paid >= net_salary`

---

## Indexes

For optimal query performance:
- `idx_employee`: Fast lookup by employee
- `idx_month_year`: Fast filtering by month/year
- `idx_payment_status`: Fast filtering by payment status
- `idx_payment_date`: Fast sorting/filtering by payment date
- `idx_created_at`: Fast sorting by creation time

---

## Sample Queries

### Get Employee Total Paid and Upcoming Payment
```sql
SELECT 
    SUM(amount_paid) AS total_paid,
    SUM(net_salary - amount_paid) AS upcoming_payment
FROM payroll_payroll
WHERE employee_id = 5
AND payment_status IN ('pending', 'partial');
```

### Get All Pending Payments for Admin
```sql
SELECT 
    p.id,
    u.username,
    u.email,
    p.month,
    p.year,
    p.net_salary,
    p.amount_paid,
    (p.net_salary - p.amount_paid) AS amount_pending
FROM payroll_payroll p
JOIN accounts_user u ON p.employee_id = u.id
WHERE p.payment_status IN ('pending', 'partial')
ORDER BY p.year DESC, p.month DESC;
```

### Get Payment History for a Payroll
```sql
SELECT 
    pmt.id,
    pmt.amount,
    pmt.payment_date,
    pmt.created_at,
    pmt.notes,
    u.username AS created_by
FROM payroll_payment pmt
LEFT JOIN accounts_user u ON pmt.created_by_id = u.id
WHERE pmt.payroll_id = 1
ORDER BY pmt.payment_date DESC, pmt.created_at DESC;
```

---

## Django Model Representation

The Django models (`Payroll` and `Payment`) automatically handle:
- Decimal precision (10 digits, 2 decimal places)
- Foreign key relationships
- Auto-calculation of `net_salary` and `payment_status`
- Timestamps (`created_at`, `updated_at`)

