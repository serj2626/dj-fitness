from django.urls import path
from .views import (
    ArticleListView, ArticleDetailView, AddLikeView,
    AddDislikeView, AddReview, delete_comment)

app_name = 'posts'

urlpatterns = [
    path('list/<slug:slug>', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path("add/review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path('<int:pk>/add/like', AddLikeView.as_view(), name='add_like'),
    path('<int:pk>/add/dislike/', AddDislikeView.as_view(), name='add_dislike'),
    path('<int:pk>/delete/comment/', delete_comment, name='delete_comment'),
]
