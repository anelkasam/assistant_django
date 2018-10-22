from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm


def register(request):
    """
    If user is authenticated then redirect to the index page.
    Return template with registration from.
    If form submit -> create new user and redirect to the index page.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['password2']
            user = User(**form.cleaned_data)
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    """
    Login user by username and password
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('index')
            form.add_error(None, 'Invalid login or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')
