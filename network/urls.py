from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("editPost", views.editPost, name="editPost"),
    path("follow", views.toggleFollow, name="follow"),
    path("following", views.following, name="following"),
    path("like", views.toggleLike, name="like")
]
