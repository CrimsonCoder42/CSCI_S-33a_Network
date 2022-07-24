
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("personal_profile", views.personal_profile, name="personal_profile"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("post/<int:id>", views.postEdit, name="user_profile"),
    path("follow/<str:username>", views.follow, name="create_post"),

    #API Routes

    path("post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.user_profile, name="user_profile"),
    path("likes/<int:id>", views.likes, name="likes"),
]
