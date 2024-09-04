
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("save",views.save_post, name="save_post"),

    #API calls
    path("get_posts/<str:post_type>/",views.get_posts,name="get_posts"),
    path("users/<str:usr>",views.get_user,name="get_user"),
    path("follow",views.follow,name="follow"),
    path("unfollow",views.unfollow,name="unfollow"),
    path("<str:usr>/following",views.following_page,name="following_page"),
    path("following",views.user_following,name="user_following"),
    path("edit_post/<int:id>",views.edit_post,name="edit"),
    path("get_post/<int:id>",views.get_post,name="post"),
    path("<int:id>/like",views.get_likes,name="like"),
    path("<int:id>/like_count",views.like_count,name="like_count")
]
