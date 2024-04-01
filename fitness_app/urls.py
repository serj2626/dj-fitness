from django.urls import path
from .views import (
    HomeView, TrainerListView, AbonementListView, TrainerDetailView,
    OrderAbonementCreateView, AddReview, OrderTrainingCreateView, 
    MyAbonementListView, MyTrainingListView,SuccessTemplateView, CancelTemplateView, 
    AddStarRating, DeleteAbonementView, DeleteTrainingView, CalendarTrainerView
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
    path('my-abonements/<pk>/delete/', DeleteAbonementView.as_view(), name='abonement_delete'),
    path('my-trainings/', MyTrainingListView.as_view(), name='my_trainings'),
    path('my-trainings/<pk>delete/', DeleteTrainingView.as_view(), name='training_delete'),
    path('order-success', SuccessTemplateView.as_view(), name='order_success'),
    path('order-cancel', CancelTemplateView.as_view(), name='order_cancel'),
    path('trainer/<pk>/add-rating', AddStarRating.as_view(), name='add_star_rating'),
    path('calendar/', CalendarTrainerView.as_view(), name='calendar'),
]
