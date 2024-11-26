from rest_framework import serializers, viewsets

from Access.api import SimpleEmpresaSerializer
from Access.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    empresa_data = SimpleEmpresaSerializer(read_only=True, required=False, source='empresa')

    class Meta:
        model = Producto
        fields = '__all__'


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
