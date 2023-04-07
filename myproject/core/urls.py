from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_tweet/', views.create_tweet, name='create_tweet'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
    path('register/', views.register, name='register'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
