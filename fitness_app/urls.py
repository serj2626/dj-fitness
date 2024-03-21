from django.urls import path
from .views import (
    HomeView, TrainerListView, AbonementListView, TrainerDetailView,
    OrderAbonementCreateView, AddReview, OrderTrainingCreateView, MyAbonementListView
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('trainers/', TrainerListView.as_view(), name='trainer_list'),
    path('abonements/', AbonementListView.as_view(),
         name='abonements'),
    path('trainers/<pk>/', TrainerDetailView.as_view(), name='trainer_detail'),
    path('order/abonement/create', OrderAbonementCreateView.as_view(),
         name='order_abonement_create'),
    path('trainers/<pk>/review/add', AddReview.as_view(), name='add_review'),
    path('order/training/create', OrderTrainingCreateView.as_view(), name='order_training'),
    path('my-abonements/', MyAbonementListView.as_view(), name='my_abonements'),
    path('trainings/', HomeView.as_view(), name='trainings'),
]
