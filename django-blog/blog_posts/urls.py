from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("all/", views.PostListView.as_view(), name="all"),
    path("user/me", views.my_post_list_view, name="my-posts"),
    path("user/<int:pk>", views.UserPostListView.as_view(), name="user"),
    path("create/", views.create_post_view, name="create"),
    path("search/", views.search_post_view, name="search"),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("<int:post_id>/comment/", views.create_comment_view, name="new-comment"),
]
