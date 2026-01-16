from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # 로그인/로그아웃은 Django 내장 기능 사용
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 회원가입은 우리가 직접 만듦
    path('signup/', views.signup, name='signup'),
]