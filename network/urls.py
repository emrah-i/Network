
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('get-csrf-token', views.get_csrf_token, name='get-csrf-token'),
    path("posts", views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("acc/<str:username>", views.account, name="account"),
    path("following", views.following, name="following"),
    path("following_posts/<int:start>/<str:sort>", views.following_posts, name="following_posts"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("edit_comment/<int:comment_id>", views.edit_comment, name="edit_comment"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("unfollow/<int:user_uf>", views.unfollow, name="unfollow"),
    path("remove/<int:user_uf>", views.remove, name="remove"),
    path("follow/<int:user_f>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("category_posts/<str:category>/<int:start>/<str:sort>", views.category_posts, name="category_posts"),
    path("search_page", views.search_page, name="search_page"),
    path("search/<str:query>", views.search, name="search"),
    path("comment/<str:commentid>", views.comment, name="comment"),
    path("reply/<int:commentid>", views.reply, name="reply"),
    path("auth", views.auth, name="auth")
]
