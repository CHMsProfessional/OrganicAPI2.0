from django.db import models

from Access.models import Producto, CarritoCompra


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(CarritoCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.carrito.total_puntos() + self.producto.costo_puntos > self.carrito.suscripcion.monto_total_puntos:
            raise ValueError("El total de puntos excede el límite permitido por la suscripción.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} en {self.carrito}"
