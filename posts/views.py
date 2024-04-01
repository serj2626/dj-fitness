from email import message
from unicodedata import category

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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


class ArticleDetailView(TitleMixin, DetailView):
    model = Article
    template_name = "posts/article_detail.html"
    context_object_name = "article"
    title = "Статья"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['reviews'] = Comment.objects.filter(
            article=self.get_object(), parent__isnull=True)
        return context


class AddReview(View, LoginRequiredMixin):
    """Оставить отзыв о статье"""

    def post(self, request, pk):
        article = Article.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
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


def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))