from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
import uuid
from datetime import timedelta
from .models import EmailVerification
from django.utils import timezone
from fitness_project.settings import EMAIL_HOST_USER

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control,', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(
                "Пользователь с такой почтой уже существует")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'ipeg'], message='Фото должно быть в формате jpd или jpeg.')])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'age', 'phone', 'avatar')
        widgets = {

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Возраст'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),

        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not 18 <= age <= 75:
            raise forms.ValidationError("Возраст указан неверно")
        return age
