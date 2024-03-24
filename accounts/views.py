from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm, ProfileUpdateForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import EmailVerification
from django.utils import timezone
from fitness_project.settings import EMAIL_HOST_USER
from datetime import timedelta
import uuid

from django.urls import reverse_lazy
from common.mixins import TitleMixin


from django.views.generic import FormView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView


User = get_user_model()


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser = authenticate(email=email, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Пользователь успешно вошел в аккаунт")
            return redirect('home')
        else:
            messages.error(request, "Не удалось войти в аккаунт")
            return redirect('login')

    return render(request, "accounts/login.html")


class RegisterView(TitleMixin, SuccessMessageMixin, FormView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Вы успешно зарегистрировались!'
    title = 'Регистрация'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()

        expiration = timezone.now() + timedelta(days=2)
        token = uuid.uuid4()
        record = EmailVerification.objects.create(
            user=new_user, token=token, expiration=expiration)
        record.send_verification_email()

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    title = 'Профиль'


class ProfileUpdateView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(form.cleaned_data.get('avatar'))
        return super().form_valid(form)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'email/email_verification.html'
    title = 'Подтверждение почты'

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        email = kwargs['email']

        user = User.objects.get(email=email)
        email_verification = EmailVerification.objects.filter(
            user=user, token=token)

        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified = True
            user.save()
            return super().get(request, *args, **kwargs)
        return redirect('home')
