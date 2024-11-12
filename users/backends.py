from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from .models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        try:
            user = User.objects.get(email = username)
        except User.DoesNotExist:
            return None
        
        if user and check_password(password,user.password):
            return user
        
        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None