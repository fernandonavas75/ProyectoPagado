from django.db import models

# Create your models here.
from django.db import models

# Modelo de Usuarios (Clientes y Empleados)
class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
    ]

    nombre_usuario = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre_usuario


# Modelo del Menú (Platos disponibles)
class Menu(models.Model):
    nombre_plato = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(default=0)
    recomendado = models.BooleanField(default=False)
    imagen_url = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_plato


# Modelo de Pedidos
class Pedido(models.Model):
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    codigo_recogida = models.CharField(max_length=10, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.id_cliente.nombre_usuario}"


# Modelo de Detalles del Pedido
class DetallePedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Pedido {self.id} - Producto: {self.id_producto.nombre_plato}"


# Modelo de Recargas de Saldo
class Recarga(models.Model):
    id_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="recargas_cliente")
    id_empleado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name="recargas_empleado")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recarga de {self.monto} a {self.id_cliente.nombre_usuario}"


# Modelo de Balance Diario
class Balance(models.Model):
    fecha = models.DateField(unique=True)
    ventas_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    recargas_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Balance {self.fecha} - Ventas: {self.ventas_total}, Recargas: {self.recargas_total}"
