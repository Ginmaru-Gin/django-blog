from dataclasses import dataclass
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse


def dev_index(request: HttpRequest):
    @dataclass
    class Option:
        text: str
        url: str

    options = {
        "Все посты": "posts:all",
        "Поиск постов": "posts:search",
    }
    if request.user.is_authenticated:
        options.update(
            {
                "Мои посты": "posts:my-posts",
                "Новый пост": "posts:create",
                "Изменить пароль": "users:change_pass",
                "Выйти": "users:logout",
            }
        )
    else:
        options.update(
            {
                "Войти": "users:login",
                "Зарегистрироваться": "users:register",
            }
        )
    options = [Option("Админка", "/admin/")] + [
        Option(k, reverse(v)) for k, v in options.items()
    ]
    return render(
        request,
        "dev-index.html",
        {"options": options},
    )
