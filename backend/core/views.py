from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Usuario, Menu, Pedido, DetallePedido, Recarga, Balance
from .serializers import UsuarioSerializer, MenuSerializer, PedidoSerializer, DetallePedidoSerializer, RecargaSerializer, BalanceSerializer

# Vista para Usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Vista para el Menú
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

# Vista para Pedidos
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

# Vista para Detalles de Pedido
class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

# Vista para Recargas
class RecargaViewSet(viewsets.ModelViewSet):
    queryset = Recarga.objects.all()
    serializer_class = RecargaSerializer

# Vista para el Balance
class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
