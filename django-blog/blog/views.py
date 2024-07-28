from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user
from django.http import HttpRequest
from django.shortcuts import render

from utils.utils import requestUsername


def dev_index(request: HttpRequest):
    return render(request, "dev-index.html", {"username": requestUsername(request)})
