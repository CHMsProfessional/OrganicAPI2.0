from django.contrib.auth.models import User
from django.db import models


class Newsletter(models.Model):
    correo = models.EmailField(unique=True)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.correo
