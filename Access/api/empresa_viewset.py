from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Access.api import ProductoSerializer
from Access.api.simple_serializers import SimpleUsuarioSerializer, SimpleProductoSerializer, \
    SimpleSuscripcionSerializer, SimpleNoticiaSerializer
from Access.models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    propietario_data = SimpleUsuarioSerializer(read_only=True, source='propietario', required=False)

    class Meta:
        model = Empresa
        fields = '__all__'


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def create(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.validated_data['propietario']
        usuario.has_Empresa = True
        usuario.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data['propietario'])

        if 'propietario' in request.data:
            usuarioAntiguo = instance.propietario
            usuarioAntiguo.has_Empresa = False
            usuarioAntiguo.save()

            usuario = serializer.validated_data['propietario']
            usuario.has_Empresa = True
            usuario.save()

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        usuario = instance.propietario
        usuario.has_Empresa = False
        usuario.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='productos')
    def empresa_productos(self, request, pk=None):
        empresa = self.get_object()
        productos = empresa.productos.all()
        serializer = SimpleProductoSerializer(productos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='suscripciones')
    def empresa_suscripciones(self, request, pk=None):
        empresa = self.get_object()
        suscripciones = empresa.suscripciones.all()
        serializer = SimpleSuscripcionSerializer(suscripciones, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='noticias')
    def empresa_noticias(self, request, pk=None):
        empresa = self.get_object()
        noticias = empresa.noticias.all()
        serializer = SimpleNoticiaSerializer(noticias, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
