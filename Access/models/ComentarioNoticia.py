from django.db import models

from Access.models import Noticia, Usuarios


class ComentarioNoticia(models.Model):
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='comentarios')
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.user.username} en {self.noticia.titulo}"
