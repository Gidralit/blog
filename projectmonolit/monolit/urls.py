from tkinter.font import names
from venv import create

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('deleteaccount/', views.delete_account, name="delete_account"),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create', views.create_post, name='create_post'),
    path('post/edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment')
]