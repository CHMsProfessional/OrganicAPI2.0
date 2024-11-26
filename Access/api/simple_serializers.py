from django.contrib.auth.models import User
from rest_framework import serializers

from Access.models import Empresa, Usuarios, MetodoPago, SuscripcionEmpresa, Producto, Noticia


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class SimpleUsuarioSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Usuarios
        fields = ('id', 'user', 'is_Admin', 'has_Empresa')


class SimpleMetodoPagoSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = MetodoPago
        fields = ('id','nombre_titular', 'user', 'fecha_expiracion')


class SimpleSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuscripcionEmpresa
        fields = ('id','nombre', 'frecuencia', 'monto_total_puntos')

class SimpleProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'descripcion','costo_puntos')


class SimpleEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('id', 'nombre', 'direccion', 'telefono')

class SimpleNoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ('id', 'titulo', 'contenido', 'fecha_publicacion')
