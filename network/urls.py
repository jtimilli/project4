
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name='following'),
    path("profile/<str:username>", views.profile, name="profile"),


# API Routes
    path('post', views.getPost, name="post"),
    path('newpost', views.newPost, name="newpost"),
    path('togglefollow/<str:username>', views.toggleFollow, name="togglefollow"),
    path('likes/<int:id>/', views.toggleLike, name="toggleLike")
]