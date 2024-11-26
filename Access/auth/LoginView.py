import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View

from Access.models import Usuarios


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        # Intenta cargar los datos JSON desde el cuerpo de la solicitud
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Solicitud inválida. Formato JSON incorrecto.'}, status=400)

        # Imprime los valores recibidos para depuración
        print(username)
        print(password)

        # Autentica al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                usuario_extendido = user.usuarios
                es_admin = usuario_extendido.is_Admin
                tiene_empresa = usuario_extendido.has_Empresa
            except Usuarios.DoesNotExist:
                es_admin = False
                tiene_empresa = False

            return JsonResponse({
                'message': 'Inicio de sesion exitoso',
                'username': user.username,
                'is_admin': es_admin,
                'has_empresa': tiene_empresa
            }, status=200)
        else:
            # Respuesta en caso de credenciales incorrectas
            return JsonResponse({'message': 'Credenciales invalidas'}, status=401)
