from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import User
from .forms import UserRegisterForm, UserLoginForm, OTPVerificationForm
import random


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        otp = request.POST.get('otp')
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            if otp:
                # Verify OTP
                if (request.session.get('registration_email') == email and 
                    request.session.get('registration_username') == username and
                    request.session.get('registration_otp') == otp):
                    user = form.save(commit=False)
                    user.is_active = True
                    user.save()
                    # Clear session
                    del request.session['registration_email']
                    del request.session['registration_username']
                    del request.session['registration_otp']
                    login(request, user)
                    messages.success(request, 'Registration successful. Welcome!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid OTP')
            else:
                messages.error(request, 'Please enter OTP')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        if email and username:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Employee ID already taken'})
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            # Store in session or temp storage
            request.session['registration_otp'] = otp
            request.session['registration_email'] = email
            request.session['registration_username'] = username
            # Send email
            subject = 'Your OTP for DayFlow Registration'
            message = f'Your OTP is: {otp}'
            send_mail(subject, message, 'noreply@dayflow.com', [email])
            return JsonResponse({'success': True, 'message': 'OTP sent to your email'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                user = User.objects.get(email_verification_token=otp, is_active=False)
                user.is_active = True
                user.email_verification_token = None
                user.save()
                login(request, user)
                messages.success(request, 'Email verified successfully. Welcome!')
                return redirect('dashboard')
            except User.DoesNotExist:
                messages.error(request, 'Invalid OTP.')
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_otp.html', {'form': form})