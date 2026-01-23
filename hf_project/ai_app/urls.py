from django.urls import path
from django.contrib.auth.views import LogoutView 
from . import views

urlpatterns = [
    path('sentiment/', views.sentiment_view, name='sentiment'), # Public
    path('summarize/', views.summary_view, name='summary'),     # Private
    path('translate/', views.translate_view, name='translate'), # Private
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]