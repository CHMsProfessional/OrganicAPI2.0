from django.contrib.auth.models import User
from django.db import models

from Access.models import Usuarios


class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    propietario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='empresas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
