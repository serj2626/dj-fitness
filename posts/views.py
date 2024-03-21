from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from common.mixins import TitleMixin
from .models import Article
from django.views import View
from django.views.generic import DetailView


class ArticleListView(TitleMixin, View):
    def get(self, request, slug):
        articles = Article.objects.filter(category__slug=slug)
        return render(request, 'posts/article_list.html', {'articles': articles, 'title': 'Статьи'})


class ArticleDetailView(DetailView):
    model = Article
    template_name = "posts/article_detail.html"
    context_object_name = "article"
    title = "Статья"