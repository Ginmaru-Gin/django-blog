from datetime import datetime
from typing import Any
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from .models import Post
from .forms import CreatePostForm, SearchPostForm

from utils.utils import requestUsername


# Create your views here.
class PostView(DetailView):
    model = Post

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["username"] = requestUsername(self.request)
        return context


class PostListView(ListView):
    model = Post
    template_name = "posts/all_list.html"
    ordering = "-date"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["username"] = requestUsername(self.request)
        return context


@login_required(login_url=reverse_lazy("users:login"))
def create_post_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
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
        "posts/create-post.html",
        {"form": form, "username": requestUsername(request)},
    )


def search_post_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SearchPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            q = Post.objects.all()
            if data.get("author"):
                q = q.filter(author__username__iexact=data.get("author"))
            if data.get("header"):
                q = q.filter(header__icontains=data.get("header"))
            if data.get("text"):
                q = q.filter(text__icontains=data.get("text"))
            return render(
                request,
                "posts/search.html",
                {
                    "form": SearchPostForm(),
                    "username": requestUsername(request),
                    "result": q,
                },
            )
        else:
            return render(
                request,
                "posts/search.html",
                {"form": SearchPostForm(), "username": requestUsername(request)},
            )

    else:
        return render(
            request,
            "posts/search.html",
            {"form": SearchPostForm(), "username": requestUsername(request)},
        )
