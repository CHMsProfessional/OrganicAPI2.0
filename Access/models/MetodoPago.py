from django.db import models

from Access.models import Usuarios


class MetodoPago(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="metodos_pago")
    nombre_titular = models.CharField(max_length=100)  # Nombre del titular de la tarjeta
    numero_tarjeta = models.CharField(max_length=16)  # Número de tarjeta (enmascarado por seguridad)
    fecha_expiracion = models.CharField(max_length=5)  # Fecha de expiración (MM/AA)
    cvv = models.CharField(max_length=3)  # CVV de la tarjeta
    es_visa = models.BooleanField(default=True)  # Confirmación de que es tarjeta Visa
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_titular} - **** **** **** {self.numero_tarjeta[-4:]}"
