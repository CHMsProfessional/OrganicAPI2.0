from rest_framework import serializers, viewsets

from Access.models import MetodoPago


class MetodoPagoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MetodoPago
        fields = '__all__'


class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
