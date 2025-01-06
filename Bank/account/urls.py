from django.urls import path,include
from .views import UserRegistrationView,PassChangeView,UserLogoutView,UserLoginView,UserBankAccountUpdateView


urlpatterns = [
    path('register',UserRegistrationView.as_view(),name='register'),
    path('profile',UserBankAccountUpdateView.as_view(),name='profile'),
    path('login',UserLoginView.as_view(),name='login'),
    path('changepass',PassChangeView.as_view(),name='changepass'),
    path('logout',UserLogoutView.as_view(),name='logout'),
   
]
