from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Enter password again'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('image', 'username', 'email')
