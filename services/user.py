from django.contrib.auth import get_user_model
from django.db import models
from typing import Optional


def create_user(
    username: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
) -> None:
    User = get_user_model()
    User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name or "",
        last_name=last_name or "",
        email=email or "",
    )


def get_user(user_id: int) -> models.Model:
    User = get_user_model()
    return User.objects.get(id=user_id)


def update_user(
    user_id: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> None:
    user = get_user(user_id)
    if username:
        user.username = username
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if password:
        user.set_password(password)
    user.save()
