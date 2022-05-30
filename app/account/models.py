from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    
    def new_token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh), str(refresh.access_token)
