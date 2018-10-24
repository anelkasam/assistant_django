from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed

from .forms import RegisterForm, EditUserForm, ProfileForm, CreateFamilyForm, TokenForm
from .models import Family


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


@login_required
def profile_page(request):
    """"""
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_page')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_page.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@login_required
def create_family(request):
    if request.user.profile.family:
        return redirect('index')

    if request.method == 'POST':
        form = CreateFamilyForm(request.POST)
        if form.is_valid():
            form.save(request.user.profile)

            return redirect('profile_page')
    else:
        form = CreateFamilyForm()

    return render(request, 'create_family.html', {'form': form})


@login_required
def leave_family(request):
    """
    If user belong to some family and not an admin -> set family None
    If user is admin -> do nothing for now
    """
    profile = request.user.profile
    if not profile.family:
        return redirect('index')

    if not profile.is_admin:
        profile.family = None
        profile.save()

    return redirect('profile_page')


@login_required
def create_token(request):
    """
    Create token for connection to the family
    """
    profile = request.user.profile
    if not (profile.family and profile.is_admin):
        return redirect('profile_page')

    return HttpResponse(profile.family.generate_token())


@login_required
def connect_to_family(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed('POST')

    token = request.POST.get('token')
    if not token:
        # ToDo: Return the error message also!!!
        return redirect('profile_page')

    family = Family.verify_token(token)
    if not family:
        # ToDo: Return the error message also!!!
        return redirect('profile_page')

    request.user.profile.family = family
    request.user.profile.save()
    return redirect('profile_page')
