from rest_framework import serializers, viewsets

from Access.models import ComentarioNoticia


class ComentarioNoticiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComentarioNoticia
        fields = '__all__'


class SuscripcionEmpresaViewSet(viewsets.ModelViewSet):
    queryset = ComentarioNoticia.objects.all()
    serializer_class = ComentarioNoticiaSerializer
