from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render


def register(request):
    return render(request, 'register.html')


def login_user(request):
    pass


def logout_user(request):
    pass
