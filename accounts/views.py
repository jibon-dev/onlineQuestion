from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Registration Successfully Completed, Check Your Email To Activate Your Account')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {email}")
                return redirect('home')
            else:
                messages.add_message(request, messages.WARNING, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    messages.add_message(request, messages.WARNING, "You have successfully logged out!")
    logout(request)
    return redirect('home')

