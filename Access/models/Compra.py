from django.db import models

from Access.models import Usuarios, SuscripcionEmpresa, Producto, MetodoPago


class Compra(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='compras')
    suscripcion = models.ForeignKey(SuscripcionEmpresa, on_delete=models.CASCADE, related_name='compras')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, related_name='pagos', null=True, blank=True)
    productos = models.ManyToManyField(Producto)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_validez = models.DateField()  # Fecha en la que expira la suscripción

    def obtener_costo_total(self):
        costo_puntos_total = 0
        for producto in self.productos.all():
            costo_puntos_total += producto.costo_puntos

        suscripcion = self.suscripcion
        costo_total_porcentaje = (costo_puntos_total * 100) / suscripcion.monto_total_puntos
        costo_total = (suscripcion.costo * costo_total_porcentaje) / 100
        return costo_total

    def __str__(self):
        return f"Compra de {self.usuario.user.username} - {self.suscripcion.nombre}"
