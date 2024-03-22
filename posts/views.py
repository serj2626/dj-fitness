from email import message
from typing import Any
from unicodedata import category
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from common.mixins import TitleMixin
from posts.forms import CommentForm
from .models import Article, Comment
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .service import add_like, add_dislike


class ArticleListView(TitleMixin, View):
    def get(self, request, slug):
        articles = Article.objects.filter(category__slug=slug)
        category = articles.first().category
        return render(request, 'posts/article_list.html',
                      {'articles': articles, 'title': 'Статьи', 'category': category})


class ArticleDetailView(DetailView):
    model = Article
    template_name = "posts/article_detail.html"
    context_object_name = "article"
    title = "Статья"


class CommentListView(View):

    def get(self, request, pk):
        form = CommentForm()
        article = Article.objects.get(id=pk)
        comments = Comment.objects.filter(article=article)
        return render(request, 'posts/comment_list.html',
                      {'comments': comments, 'title': 'Комментарии',
                       'article': article, 'form': form
                       })

    def post(self, request, pk):
        article = Article.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form = form.save(commit=False)
            form.text = cd.get('text')
            form.article = article
            form.user = request.user
            form.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AddLikeView(LoginRequiredMixin, DetailView):
    '''Лайк к посту'''

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        add_like(request, article)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AddDislikeView(LoginRequiredMixin, DetailView):
    '''Дизлайк к посту'''

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        add_dislike(request, article)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
