from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Access.api import SimpleUserSerializer, MetodoPagoSerializer, EmpresaSerializer
from Access.api.newsletter_viewset import NewsletterSerializer
from Access.models import Usuarios


class UsuarioSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Usuarios
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        email = validated_data.pop('email', None)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        access = Usuarios.objects.create(user=user, **validated_data)
        return access


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        response = self.check_permissions(request)
        if response:
            return response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        user = instance.user
        if 'username' in request.data:
            user.username = request.data.get('username')
        if 'first_name' in request.data:
            user.first_name = request.data.get('first_name')
        if 'last_name' in request.data:
            user.last_name = request.data.get('last_name')
        if 'email' in request.data:
            user.email = request.data.get('email')

        user.save()
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        self.perform_destroy(instance)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='empresas')
    def empresas_user(self, request, pk=None):
        user = self.get_object()
        empresas = user.empresas.all()
        if not empresas:
            return Response({'error': 'User has no companies'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get_metodos_pago')
    def get_metodo_pago(self, request, pk=None):
        user = self.get_object()
        metodo_pago = user.metodos_pago
        if not metodo_pago:
            return Response({'error': 'User has no payment methods'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MetodoPagoSerializer(metodo_pago, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='add_metodo_pago')
    def add_metodo_pago(self, request, pk=None):
        user = self.get_object()
        metodo_pago = MetodoPagoSerializer(data=request.data)

        # Validar los datos del método de pago
        if not metodo_pago.is_valid():
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el número de tarjeta ya existe para el usuario
        if user.metodos_pago.filter(numero_tarjeta=metodo_pago.validated_data['numero_tarjeta']).exists():
            return Response({'error': 'Payment method already added'}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar el nuevo método de pago
        metodo_pago_obj = metodo_pago.save()
        user.metodos_pago.add(metodo_pago_obj)
        return Response({'message': 'Payment method added successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='delete_metodo_pago')
    def delete_metodo_pago(self, request, pk=None):
        user = self.get_object()
        metodo_pago = user.metodos_pago.filter(id=request.data.get('metodo_pago_id')).first()
        if not metodo_pago:
            return Response({'error': 'Payment method not found'}, status=status.HTTP_404_NOT_FOUND)
        metodo_pago.delete()
        return Response({'message': 'Payment method deleted successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update_metodo_pago')
    def update_metodo_pago(self, request, pk=None):
        user = self.get_object()
        metodo_pago = user.metodos_pago.filter(id=request.data.get('metodo_pago_id')).first()
        if not metodo_pago:
            return Response({'error': 'Payment method not found'}, status=status.HTTP_404_NOT_FOUND)

        metodo_pago_serializer = MetodoPagoSerializer(metodo_pago, data=request.data, partial=True)

        if not metodo_pago_serializer.is_valid():
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        metodo_pago_serializer.save()
        return Response({
            'message': 'Payment method updated successfully',
            'data': metodo_pago_serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add_email_newsletter')
    def add_email_newsletter(self, request, pk=None):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        email_serializer = NewsletterSerializer(data={'correo': email})
        if not email_serializer.is_valid():
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if email_serializer.validated_data['correo'] in [email.correo for email in
                                                         email_serializer.Meta.model.objects.all()]:
            return Response({'error': 'Email already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

        email_serializer.save()

        return Response({
            'message': 'Email added to newsletter successfully',
            'data': email_serializer.data
        }, status=status.HTTP_200_OK)
