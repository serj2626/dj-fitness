from django.urls import path
from .views import ArticleListView, ArticleDetailView, CommentListView, AddLikeView, AddDislikeView, AddReview

app_name = 'posts'

urlpatterns = [
    path('list/<slug:slug>', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/comments/', CommentListView.as_view(), name='comment_list'),
    path("add/review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path('<int:pk>/add/like', AddLikeView.as_view(), name='add_like'),
    path('<int:pk>/add/dislike/', AddDislikeView.as_view(), name='add_dislike'),
]
