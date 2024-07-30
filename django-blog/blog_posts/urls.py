from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("all/", views.PostListView.as_view(), name="all"),
    path("user/", views.UserPostListView.as_view(), name="user"),
    path("create/", views.create_post_view, name="create"),
    path("search/", views.search_post_view, name="search"),
]
