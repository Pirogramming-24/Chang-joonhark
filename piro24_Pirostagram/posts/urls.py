from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
   
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('update/<int:pk>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    
    path('comment/create/<int:pk>/', views.comment_create, name='comment_create'),
    path('comment/update/<int:pk>/', views.comment_update, name='comment_update'),
    path('comment/delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    
    path('like/ajax/', views.post_like_ajax, name='post_like_ajax'),
]