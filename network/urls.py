
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("personal_profile", views.personal_profile, name="personal_profile"),

    #API Routes

    path("post", views.create_post, name="create_post"),
    path("profile/<str:username>", views.user_profile, name="user_profile"),
    path("likes/<int:id>", views.likes, name="likes"),
]
