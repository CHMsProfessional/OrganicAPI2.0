from rest_framework import serializers, viewsets

from Access.models import CarritoProducto


class CarritoProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarritoProducto
        fields = '__all__'


class CarritoProductoViewSet(viewsets.ModelViewSet):
    queryset = CarritoProducto.objects.all()
    serializer_class = CarritoProductoSerializer
