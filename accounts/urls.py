from django.urls import path
from .views import (login_view, logout_view, RegisterView, ProfileView,
                    ProfileUpdateView, EmailVerificationView)
# from django.contrib.auth.views import LoginView


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<pk>/update', ProfileUpdateView.as_view(), name='profile_edit'),
    
    path('verify/<str:email>/<uuid:token>/',
         EmailVerificationView.as_view(), name='email_verification'),

]
