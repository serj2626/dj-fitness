from django.db import models


class NewsLetter(models.Model):
    email = models.EmailField('Email')

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.email


class FeedBack(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Почта')
    subject = models.CharField('Тема сообщения', max_length=100)
    message = models.TextField('Сообщение', max_length=5000)

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return f'{self.name} - {self.subject}'
