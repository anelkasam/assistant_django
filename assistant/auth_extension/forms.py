from django import forms
from django.contrib.auth.models import User
from .models import Profile, Family


class RegisterForm(forms.Form):
    """
    Create registration form
    """
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='Email address')
    first_name = forms.CharField(label='First name', max_length=20, required=False)
    last_name = forms.CharField(label='Last name', max_length=30, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')

    def clean(self):
        """
        Check that given email isn't in the database
        Check if password equals to password2
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email):
            self.add_error('email', 'User with given email address is already registered.')

        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            self.add_error('password2', 'Please check the confirmation password.')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)


class CreateFamilyForm(forms.ModelForm):
    def save(self, profile, commit=True):
        family = super(CreateFamilyForm, self).save()
        profile.family = family
        profile.is_admin = True
        profile.save()
        return family

    class Meta:
        model = Family
        fields = ('last_name',)


class TokenForm(forms.Form):
    token = forms.CharField(label='Token')
