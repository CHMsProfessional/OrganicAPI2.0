from rest_framework import serializers, viewsets

from Access.api import SimpleEmpresaSerializer
from Access.models import SuscripcionEmpresa


class SuscripcionEmpresaSerializer(serializers.ModelSerializer):
    empresas_data = SimpleEmpresaSerializer(read_only=True, source='empresas')

    class Meta:
        model = SuscripcionEmpresa
        fields = '__all__'


class SuscripcionEmpresaViewSet(viewsets.ModelViewSet):
    queryset = SuscripcionEmpresa.objects.all()
    serializer_class = SuscripcionEmpresaSerializer
