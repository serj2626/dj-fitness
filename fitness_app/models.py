from random import choice
from django.db import models
from django.contrib.auth import get_user_model
from traitlets import default
from .service import get_path_for_avatar_for_trainer
import uuid
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Rate(models.Model):
    # Цены индивидульных тренировок

    title = models.CharField('Название тарифа', max_length=100)
    count_minutes = models.SmallIntegerField('Количество минут', null=True)
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2, default=1000)
    description = models.TextField('Описание тарифа', blank=True)

    class Meta:
        verbose_name = 'Тариф тренера'
        verbose_name_plural = 'Тарифы тренеров'
        ordering = ['-price']

    def __str__(self):
        return self.title


class Trainer(models.Model):
    # Тренер

    POSITIONS = [
        ('fitness', 'Тренер тренажерного зала'),
        ('pool', 'Инструктор бассейна'),
        ('yoga', 'Инструктор йоги'),
        ('groups', 'Тренер групповых тренировок'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.CharField('Должность', max_length=100, choices=POSITIONS)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=11, unique=True)
    rate = models.ForeignKey(
        Rate, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тариф')
    avatar = models.ImageField('Аватар',
                               upload_to=get_path_for_avatar_for_trainer,
                               default='trainers/trainer.jpg', blank=True)
    bio = models.TextField('Биография', blank=True)
    experience = models.SmallIntegerField('Опыт', default=0, null=True)

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.position}'

    def get_absolute_url(self):
        return reverse("trainer_detail", kwargs={"pk": self.pk})


class TrainerImages(models.Model):
    """Фото тренера"""
    title = models.CharField("Заголовок", max_length=100, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="trainers/images/")
    trainer = models.ForeignKey(
        Trainer, verbose_name="Тренер", on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото тренра"
        verbose_name_plural = "Фото тренеров"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class RatingTrainer(models.Model):
    """Рейтинг тренера"""
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, verbose_name="тренер")
    ip = models.CharField("IP адрес", max_length=15)

    class Meta:
        verbose_name = "Рейтинг тренера"
        verbose_name_plural = "Рейтинг тренеров"

    def __str__(self):
        return f"{self.star} - {self.trainer}"

    class Meta:
        verbose_name = "Рейтинг тренера"
        verbose_name_plural = "Рейтинг тренеров"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    trainer = models.ForeignKey(
        Trainer, verbose_name="тренер", on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(
        verbose_name="Создано", default=timezone.now)

    class Meta:
        verbose_name = "Отзыв о тренерах"
        verbose_name_plural = "Отзывы о тренерах"

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Abonement(models.Model):
    """Абонементы"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    number_of_months = models.SmallIntegerField("Количество месяцев")

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"
        ordering = ["pk"]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"
        ordering = ["-price"]


class OrderAbonement(models.Model):
    """Забронировать абонемент"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets")
    abonement = models.ForeignKey(
        Abonement, on_delete=models.CASCADE, related_name="abonements")
    start = models.DateTimeField('Начало', auto_now_add=True)
    end = models.DateTimeField('Конец', blank=True)
    status = models.BooleanField('Оплачен', default=False)
    active = models.BooleanField('Активен', default=False)

    class Meta:
        verbose_name = "Забронированный абонемент"
        verbose_name_plural = "Забронированные абонементы"

    def __str__(self):
        return f'Order - {self.abonement} - {self.user.email}'


class OrderTraining(models.Model):
    """Забронировать занятие"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trainings")
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="user_trainings")
    rate = models.ForeignKey(
        Rate, on_delete=models.CASCADE, related_name="user_trainings", blank=True, null=True)
    start = models.DateTimeField("Дата начала")
    end = models.DateTimeField('Конец', blank=True)
    status = models.BooleanField('Оплачен', default=False)

    class Meta:
        verbose_name = "Забронированное занятие"
        verbose_name_plural = "Забронированные занятия"

    def save(self, *args, **kwargs):
        if self.end is None:
            self.end = self.start + timedelta(minutes=self.rate.count_minutes)
        super().save(*args, **kwargs)