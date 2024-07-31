from datetime import datetime
from typing import Any
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from .models import Post, Comment
from .forms import CreatePostForm, SearchPostForm, CreateCommentForm


from utils.utils import requestUsername


class PostView(DetailView):
    model = Post
    template_name = "posts/post.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.get_object()).order_by(
            "-date"
        )
        return context


class PostListView(ListView):
    model = Post
    template_name = "posts/all_list.html"
    ordering = "-date"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.all().order_by("-date")
        return context


class UserPostListView(LoginRequiredMixin, PostListView):
    template_name = "posts/user_post_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(
            author__pk=self.kwargs.get("pk"),
        ).order_by(self.ordering)


def my_post_list_view(request: HttpRequest) -> HttpResponseRedirect:
    return redirect(reverse("posts:user", kwargs={"pk": get_user(request).id}))


@login_required
def create_post_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                header=form.cleaned_data.get("header"),
                text=form.cleaned_data.get("text"),
                author=get_user(request),
                date=datetime.now(),
            )
            return HttpResponseRedirect("/posts/all")
    else:
        form = CreatePostForm()
    return render(
        request,
        "posts/create_post.html",
        {"form": form},
    )


def search_post_view(request: HttpRequest) -> HttpResponse:

    def search_Q(
        data: dict,
        *,
        fields: list[str],
        db_fields: list[str],
        strict_fields: list[str],
        strict_lookup: str,
        nonstrict_lookup: str,
    ) -> Q:
        Qr = Q()
        for f, db_f, s in zip(fields, db_fields, strict_fields):
            if data.get(f):
                Qr = Qr & Q(
                    **{
                        f"{db_f}__{strict_lookup if data.get(s) else nonstrict_lookup}": data.get(
                            f
                        )
                    }
                )
        return Qr

    if request.method == "POST":
        form = SearchPostForm(request.POST)
        if form.is_valid():
            q = Post.objects.all()
            Qr = search_Q(
                form.cleaned_data,
                fields=["author", "header", "text"],
                db_fields=["author__username", "header", "text"],
                strict_fields=["strict_author", "strict_header", "strict_text"],
                strict_lookup="exact",
                nonstrict_lookup="icontains",
            )
            q = Post.objects.filter(Qr).order_by("-date")
            return render(
                request,
                "posts/search.html",
                {
                    "form": SearchPostForm(),
                    "posts": q,
                    "comments": Comment.objects.filter(post__in=q),
                },
            )
        else:
            return render(
                request,
                "posts/search.html",
                {"form": SearchPostForm()},
            )

    return render(
        request,
        "posts/search.html",
        {"form": SearchPostForm()},
    )


@login_required
def create_comment_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get("text"),
                post=post,
                author=get_user(request),
                date=datetime.now(),
            )
            return redirect(request.GET.get("next", reverse("posts:all")))
    return render(
        request,
        "posts/create_comment.html",
        {
            "form": CreateCommentForm(),
            "post": post,
            "comments": Comment.objects.filter(post=post).order_by("-date"),
        },
    )
