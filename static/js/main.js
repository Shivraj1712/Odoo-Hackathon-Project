// DayFlow HR - Enhanced JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to page content
    const content = document.querySelector('.fade-in');
    if (content) {
        content.style.opacity = '0';
        setTimeout(() => {
            content.style.transition = 'opacity 0.6s ease';
            content.style.opacity = '1';
        }, 100);
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && form.checkValidity()) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm mr-2"></span>Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Date input validation for leave forms
    const startDateInputs = document.querySelectorAll('input[name="start_date"]');
    const endDateInputs = document.querySelectorAll('input[name="end_date"]');
    
    startDateInputs.forEach(startDate => {
        endDateInputs.forEach(endDate => {
            startDate.addEventListener('change', function() {
                if (endDate.value && this.value > endDate.value) {
                    endDate.setCustomValidity('End date must be after start date');
                } else {
                    endDate.setCustomValidity('');
                }
            });

            endDate.addEventListener('change', function() {
                if (startDate.value && this.value < startDate.value) {
                    this.setCustomValidity('End date must be after start date');
                } else {
                    this.setCustomValidity('');
                }
            });
        });
    });
});
