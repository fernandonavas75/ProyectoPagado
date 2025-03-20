from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("El correo electrónico es obligatorio."))
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError(_("La contraseña es obligatoria."))

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario con permisos de administración."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True."))

        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("Correo Electrónico"))
    first_name = models.CharField(max_length=30, verbose_name=_("Nombre"), blank=True, null=True)
    last_name = models.CharField(max_length=30, verbose_name=_("Apellido"), blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Saldo Disponible"))

    is_active = models.BooleanField(default=True, verbose_name=_("Activo"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Miembro del personal"))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_("Fecha de Registro"))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_("Último Acceso"))

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuarios_personalizados",
        blank=True,
        verbose_name=_("Grupos"),
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuarios_personalizados",
        blank=True,
        verbose_name=_("Permisos de Usuario"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"



class Menu(models.Model):
    nombre_plato = models.CharField(max_length=100, verbose_name=_("Nombre del Plato"))
    descripcion = models.TextField(verbose_name=_("Descripción"))
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Precio"))
    cantidad_disponible = models.IntegerField(default=0, verbose_name=_("Cantidad Disponible"))
    recomendado = models.BooleanField(default=False, verbose_name=_("Recomendado"))
    imagen = models.URLField(blank=True, null=True, verbose_name=_("Imagen del Plato"))

    def __str__(self):
        return self.nombre_plato



class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ("Pendiente", "Pendiente"),
        ("Entregado", "Entregado"),
        ("Cancelado", "Cancelado"),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Pedido"))
    codigo_recogida = models.CharField(max_length=10, unique=True, verbose_name=_("Código de Recogida"))
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total del Pedido"))
    estado_pedido = models.CharField(max_length=10, choices=ESTADOS_PEDIDO, default="Pendiente", verbose_name=_("Estado del Pedido"))

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.email}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles", verbose_name=_("Pedido"))
    producto = models.ForeignKey(Menu, on_delete=models.PROTECT, verbose_name=_("Producto"))
    cantidad = models.PositiveIntegerField(verbose_name=_("Cantidad"))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Subtotal"))

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_plato} (Pedido {self.pedido.id})"


class Recarga(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="recargas", verbose_name=_("Cliente"))
    empleado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name="recargas_realizadas", verbose_name=_("Empleado"))
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monto de Recarga"))
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Recarga"))

    def __str__(self):
        return f"Recarga de ${self.monto} a {self.cliente.email}"
