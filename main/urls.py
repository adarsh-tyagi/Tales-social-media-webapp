from os import name
from django.urls import path
from . import views

app_name="main"
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('write/', views.user_post, name="write"),
    path('profile/', views.profile, name="profile"),
    path('userpost/', views.userpost, name="userpost"),
    path('post/<int:post_pk>/delete/', views.deletepost, name="deletepost"),
    path('profile/<str:post_user>/', views.otherprofile, name="otherprofile"),
    path('comments/<int:post_obj>/', views.comments, name="comments"),
    path('comment/<int:post_obj>/', views.comment, name="comment"),
    path('follow/<str:user_name>/', views.follow_user, name="follow_user"),
    path('unfollow/<str:user_name>/', views.unfollow_user, name="unfollow_user"),
    path('<str:user_name>/follow_detail/', views.follow_detail, name="follow_detail"),
    path('<str:user_name>/tales/', views.other_tales, name="other_tales"),
    path('search_user/<str:user_name>/', views.search_user, name="search_user"),
    path('search_user/', views.empty_search, name="empty_search")
]
