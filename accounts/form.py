from django import forms
from django.forms import ModelForm, Textarea, TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="User name", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'website', 'address', 'mobile', 'fax', 'telephone')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = '__all__'
