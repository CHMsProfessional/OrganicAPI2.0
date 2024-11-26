from django.urls import path, include
from rest_framework import routers

from Access.api import UsuarioViewSet, EmpresaViewSet, ProductoViewSet, CompraViewSet, SuscripcionEmpresaViewSet, \
    CarritoProductoViewSet, CarritoCompraViewSet, UserViewSet, NoticiaViewSet
from Access.auth import LoginView

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'suscripciones_empresa', SuscripcionEmpresaViewSet)
router.register(r'noticias', NoticiaViewSet)
router.register(r'carritos_producto', CarritoProductoViewSet)
router.register(r'carritos_compra', CarritoCompraViewSet)

router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

]
