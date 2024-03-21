from django.urls import path 
from .views import  feedback_view, newsletter_view


app_name = 'contacts'

urlpatterns = [
    path('feedback/', feedback_view, name='feedback'),
    path('newsletter/', newsletter_view, name='newsletter'),
    
]
