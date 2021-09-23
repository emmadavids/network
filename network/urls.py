
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit_post", views.submit_post, name="submit"),
    path("profile/<int:id>", views.load_profile, name="load_profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following/", views.load_following, name="following"),

    #API route 
    path("editpost/<int:id>", views.edit_post, name="editpost"),
    path("like/<int:id>", views.like, name="like")
]
