from rest_framework import serializers, viewsets

from Access.models import Compra, CarritoCompra


class CarritoCompraSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarritoCompra
        fields = '__all__'


class CarritoCompraViewSet(viewsets.ModelViewSet):
    queryset = CarritoCompra.objects.all()
    serializer_class = CarritoCompraSerializer
