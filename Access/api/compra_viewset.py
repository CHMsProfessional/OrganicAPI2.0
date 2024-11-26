from rest_framework import serializers, viewsets

from Access.api.simple_serializers import SimpleUsuarioSerializer, SimpleEmpresaSerializer, SimpleMetodoPagoSerializer, \
    SimpleSuscripcionSerializer, SimpleProductoSerializer
from Access.models import Compra


class CompraSerializer(serializers.ModelSerializer):
    costo_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True,
                                           source='obtener_costo_total')
    usuario_data = SimpleUsuarioSerializer(read_only=True, source='usuario', required=False)
    empresa_data = SimpleEmpresaSerializer(read_only=True, source='empresa', required=False)
    suscripcion_data = SimpleSuscripcionSerializer(read_only=True, source='suscripcion', required=False)
    metodo_pago_data = SimpleMetodoPagoSerializer(read_only=True, source='metodo_pago', required=False)
    productos_data = SimpleProductoSerializer(read_only=True, many=True, source='productos', required=False)

    class Meta:
        model = Compra
        fields = '__all__'


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
