from django.db import models

from Access.models import Usuarios, SuscripcionEmpresa, Producto


class CarritoCompra(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='carritos')
    suscripcion = models.ForeignKey(SuscripcionEmpresa, on_delete=models.CASCADE, related_name='carritos')
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def total_puntos(self):
        return sum(producto.costo_puntos for producto in self.productos.all())

    def __str__(self):
        return f"Carrito de {self.usuario.user.username} - {self.suscripcion.nombre}"
