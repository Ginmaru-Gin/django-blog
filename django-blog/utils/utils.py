from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest


def requestUsername(request: HttpRequest) -> str:
    user = get_user(request)
    username = "" if isinstance(user, AnonymousUser) else user.username
    return username
