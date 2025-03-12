from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, MenuViewSet, PedidoViewSet, DetallePedidoViewSet, RecargaViewSet, BalanceViewSet

# Crear el router para las vistas
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'recargas', RecargaViewSet)
router.register(r'balance', BalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Agregar todas las rutas del router
]
