from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.utils import timezone
from .service import get_path_avatar_for_user
from fitness_project.settings import EMAIL_HOST_USER
from django.urls import reverse
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь почту')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField('Телефон', max_length=11,
                             unique=True, blank=True, null=True)
    first_name = models.CharField(_('имя'), max_length=30, blank=True)
    last_name = models.CharField(_('фамилия'), max_length=30, blank=True)
    age = models.SmallIntegerField('возраст', default=18, blank=True)
    avatar = models.ImageField(
        'Аватар', upload_to=get_path_avatar_for_user, default='profiles/avatar.png')
    is_verified = models.BooleanField('Подтвержден', default=False)
    club_member = models.BooleanField('Член клуба', default=False)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class EmailVerification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={
                       'email': self.user.email, 'token': self.token})
        url = f'{settings.DOMAIN_NAME}{link}'
        send_mail(
            'Подтверждение адреса электронной почты',
            f'Пожалуйста, подтвердите свою почту {self.user.email} \
            перейдя по ссылке: {url}',
            EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return self.expiration <= timezone.now()

    class Meta:
        verbose_name = 'Верификация почты'
        verbose_name_plural = 'Верификация почты'

    def __str__(self):
        return f'EmailVerification for {self.user.email}'
