from django.contrib import messages
from django.contrib.auth import (
    forms,
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib.auth.models import AnonymousUser, Group, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from rest_framework import permissions, viewsets
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


def register(request) -> HttpResponse:
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/dev/")
    else:
        form = forms.UserCreationForm()
    return render(
        request,
        "users/register.html",
        {"form": form},
    )


def login(request) -> HttpResponse:
    if request.method == "POST":
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next", reverse("dev-index")))
    return render(
        request,
        "users/login.html",
        {"form": forms.AuthenticationForm()},
    )


@login_required
def logout(request) -> HttpResponse:
    auth_logout(request)
    return redirect(reverse("dev-index"))


@login_required
def change_password(request) -> HttpResponse:
    if request.method == "POST":
        form = forms.PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль изменён!")
            return redirect(reverse("dev-index"))
    else:
        form = forms.PasswordChangeForm(request.user)
    return render(
        request,
        "users/change_password.html",
        {"form": form},
    )
