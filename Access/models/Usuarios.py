from django.contrib.auth.models import User
from django.db import models


class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_Admin = models.BooleanField(default=False)
    has_Empresa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
