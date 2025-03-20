from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Menu, Pedido, DetallePedido, Recarga

Usuario = get_user_model()

# 🔹 Serializador de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'tipo_usuario', 'saldo']

# 🔹 Serializador para registro de usuarios
class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

# 🔹 Serializador de Menú
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

# 🔹 Serializador de Pedidos
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

# 🔹 Serializador de Detalles de Pedido
class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

# 🔹 Serializador de Recargas
class RecargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recarga
        fields = '__all__'
