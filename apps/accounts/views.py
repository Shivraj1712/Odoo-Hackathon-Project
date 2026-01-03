from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import random
from .forms import UserRegisterForm, UserLoginForm, OTPVerificationForm
from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            otp = str(random.randint(100000, 999999))
            user.email_verification_token = otp
            user.save()
            subject = 'Your OTP for DayFlow Registration'
            message = f'Your OTP is: {otp}. Enter this to verify your email.'
            send_mail(subject, message, 'noreply@dayflow.com', [user.email])
            messages.success(request, 'OTP sent to your email. Please verify to complete registration.')
            return redirect('verify_otp')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


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