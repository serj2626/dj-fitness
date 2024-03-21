from django.urls import path
from .views import ArticleListView, ArticleDetailView

app_name = 'posts'

urlpatterns = [
    path('list/<slug:slug>', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
]
