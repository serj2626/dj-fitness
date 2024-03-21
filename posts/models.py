
from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field


User = get_user_model()


class Article(models.Model):
    '''
    Модель статьи
    '''

    title = models.CharField('Заголовок', max_length=100)
    content = CKEditor5Field(blank=True, verbose_name='Описание', config_name='extends')
    likes = models.ManyToManyField(User, blank=True, related_name='liles', verbose_name='лайки')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes', verbose_name='дизлайки')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''
    Модель комментария'''

    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="comments")
    text = models.TextField("Сообщение", max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ('-created_at',)

    def __str__(self):
        return f'Комментарий от {self.user} к статье {self.article.title}'
