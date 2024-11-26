from django.db import models

from Access.models import Empresa


class Noticia(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='noticias')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre}"
