from datetime import datetime
from typing import Any
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q
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
            print(f"{Qr=}")
            q = Post.objects.filter(Qr)
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
