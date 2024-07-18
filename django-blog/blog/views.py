from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import render


def dev_index(request: HttpRequest):
    user = get_user(request)
    user_name = "" if isinstance(user, AnonymousUser) else user.username
    return render(request, "dev-index.html", {"user_name": user_name})
