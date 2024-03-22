
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


User = get_user_model()


class Category(models.Model):
    '''
    Модель категории
    '''

    name = models.CharField('Название', max_length=100)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    slug = models.SlugField('URL', max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Article(models.Model):
    '''
    Модель статьи
    '''

    title = models.CharField('Заголовок статьи', max_length=100)
    image = models.ImageField('Изображение', upload_to='articles/%Y/%m/%d/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name='Категория', related_name='articles')
    content = CKEditor5Field(
        blank=True, verbose_name='Описание', config_name='extends')
    likes = models.ManyToManyField(
        User, blank=True, related_name='liles', verbose_name='лайки')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='dislikes', verbose_name='дизлайки')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:article_detail", kwargs={"pk": self.pk})


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
