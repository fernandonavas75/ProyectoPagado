#from django.shortcuts import render
from rest_framework import serializers
from .models import Usuario, Menu, Pedido, DetallePedido, Recarga, Balance

# Serializador para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

# Serializador para el modelo Menu
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

# Serializador para el modelo Pedido
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

# Serializador para el modelo DetallePedido
class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

# Serializador para el modelo Recarga
class RecargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recarga
        fields = '__all__'

# Serializador para el modelo Balance
class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
