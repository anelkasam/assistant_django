from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import RegisterForm


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
