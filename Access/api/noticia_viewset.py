from rest_framework import serializers, viewsets

from Access.api import SimpleEmpresaSerializer
from Access.models import Noticia


class NoticiaSerializer(serializers.ModelSerializer):
    empresa_data = SimpleEmpresaSerializer(read_only=True, source='empresa')

    class Meta:
        model = Noticia
        fields = '__all__'


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
