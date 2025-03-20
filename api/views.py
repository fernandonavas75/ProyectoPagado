from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Usuario, Menu, Pedido, Recarga
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#Importaciones adicionales?
from decimal import Decimal
import json
from .models import Pedido, Usuario, Menu
from django.utils.crypto import get_random_string
from django.utils.timezone import now
import datetime
from django.db.models import Sum

# ======================= 🔹 Vistas de Autenticación =======================

@csrf_exempt
def view_login(request):
    """Maneja el inicio de sesión y redirige automáticamente al dashboard correspondiente."""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # 🔹 Redirigir directamente según el tipo de usuario
            if user.is_staff:
                return redirect("dashboard_admin")
            else:
                return redirect("dashboard_usuarios")

        else:
            return render(request, "webapp/index.html", {"error": "Credenciales inválidas"})

    return render(request, "webapp/index.html")


# ======================= 🔹 Cerrar Sesión =======================

def view_logout(request):
    """Cierra la sesión del usuario y redirige a la página de inicio."""
    logout(request)
    return redirect("index")


# ======================= 🔹 Registro de Usuarios =======================

@csrf_exempt
def view_register(request):
    """Maneja el registro de usuarios."""
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        tipo_usuario = request.POST.get("tipo_usuario", "").strip()

        # Validaciones
        if not email or not password or not first_name or not last_name:
            return JsonResponse({"status": "error", "message": "Todos los campos son obligatorios"}, status=400)

        if Usuario.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "El correo ya está registrado"}, status=400)

        # Crear usuario
        usuario = Usuario.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=(tipo_usuario == "empleado")
        )

        return JsonResponse({"status": "success", "message": "Registro exitoso"})

    return render(request, "webapp/index.html")


# ======================= 🔹 Dashboard =======================

@login_required
def view_dashboard(request):
    """Muestra el panel de administración o cliente según el tipo de usuario."""
    if request.user.is_staff:
        return render(request, "webapp/dashboard_admin/admin.html")
    return render(request, "webapp/dashboard_usuarios/cliente.html")


# ======================= 🔹 Vistas de Usuario =======================

@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_usuarios(request):
    """Muestra una lista de usuarios registrados (Solo empleados)."""
    usuarios = Usuario.objects.all()
    return render(request, "webapp/dashboard_admin/usuarios.html", {"usuarios": usuarios})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_convertir_empleado(request, user_id):
    """Convierte un cliente en empleado (Solo empleados)."""
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.is_staff = True
    usuario.save()
    messages.success(request, "Usuario promovido a empleado exitosamente.")
    return redirect("dashboard_admin_usuarios")


# ======================= 🔹 Vistas de Menú =======================

def view_dashboard_menu(request):
    """Muestra la lista de productos del menú."""
    platos = Menu.objects.all()
    return render(request, "webapp/dashboard_usuarios/menu.html", {"platos": platos})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_menu(request):
    """Muestra la gestión del menú (Solo empleados)."""
    platos = Menu.objects.all()
    return render(request, "webapp/dashboard_admin/menu.html", {"platos": platos})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_agregar_plato(request):
    """Permite a los empleados agregar un nuevo plato al menú."""
    if request.method == "POST":
        nombre = request.POST["nombre_plato"]
        descripcion = request.POST["descripcion"]
        precio = request.POST["precio"]
        cantidad = request.POST["cantidad_disponible"]
        Menu.objects.create(
            nombre_plato=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad_disponible=cantidad,
        )
        messages.success(request, "Plato agregado exitosamente.")
        return redirect("dashboard_admin_gestion_menu")

    return render(request, "webapp/dashboard_admin/agregar_plato.html")


# ======================= 🔹 Vistas de Pedidos =======================

@login_required
def view_dashboard_pedidos(request):
    """Muestra los pedidos del usuario o todos los pedidos si es empleado."""
    if request.user.is_staff:
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, "webapp/dashboard_usuarios/pedidos.html", {"pedidos": pedidos})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_pedidos(request):
    """Muestra la gestión de pedidos en tiempo real (Solo empleados)."""
    pedidos = Pedido.objects.all()
    return render(request, "webapp/dashboard_admin/pedidos.html", {"pedidos": pedidos})


@login_required
def view_dashboard_detalle_pedido(request, pedido_id):
    """Muestra el detalle de un pedido específico."""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "webapp/dashboard_usuarios/detalle_pedido.html", {"pedido": pedido})


# ======================= 🔹 Vistas de Recargas =======================

# 🔹 Vista principal de gestión de recargas
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_recargas(request):
    """Muestra la gestión de recargas (Solo empleados)."""
    usuarios = Usuario.objects.filter(is_staff=False)  # Solo clientes
    recargas = Recarga.objects.all().order_by('-fecha')  # Ordenar de más reciente a más antiguo

    return render(request, "webapp/dashboard_admin/recargas.html", {
        "usuarios": usuarios,
        "recargas": recargas
    })


# 🔹 Vista para procesar la recarga de saldo
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_recargar_saldo(request):
    """Permite a los empleados recargar saldo a un cliente."""
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")
        monto = request.POST.get("monto")

        # Validaciones
        if not cliente_id or not monto:
            messages.error(request, "⚠ Debes seleccionar un cliente y un monto válido.")
            return redirect("dashboard_admin_gestion_recargas")

        try:
            cliente = get_object_or_404(Usuario, id=cliente_id)
            monto = float(monto)

            if monto <= 0:
                messages.error(request, "⚠ El monto debe ser mayor a 0.")
                return redirect("dashboard_admin_gestion_recargas")

            # Crear registro de recarga
            nueva_recarga = Recarga(cliente=cliente, empleado=request.user, monto=monto)
            nueva_recarga.save()

            # Actualizar saldo del cliente
            cliente.saldo += monto
            cliente.save()

            print(f"✅ Recarga exitosa: Cliente {cliente.email} - Monto ${monto}")
            messages.success(request, f"✅ Se recargaron ${monto:.2f} a {cliente.first_name} {cliente.last_name}.")

        except Exception as e:
            print(f"❌ Error en la recarga: {e}")
            messages.error(request, "⚠ Error al realizar la recarga.")

        return redirect("dashboard_admin_gestion_recargas")

    return redirect("dashboard_admin_gestion_recargas")


# 🔹 Vista para mostrar el historial de recargas
@login_required
def view_dashboard_historial_recargas(request):
    """Muestra el historial de recargas del usuario o de todos los clientes si es empleado."""
    if request.user.is_staff:
        recargas = Recarga.objects.all().order_by('-fecha')
    else:
        recargas = Recarga.objects.filter(cliente=request.user).order_by('-fecha')

    return render(request, "webapp/dashboard_usuarios/historial_recargas.html", {"recargas": recargas})








# 🔹 API para obtener los platos
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_obtener_platos(request):
    platos = list(Menu.objects.values())  # Convertir QuerySet en lista de diccionarios
    return JsonResponse({"platos": platos})



@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_guardar_plato(request):
    """
    Vista para agregar o actualizar un plato en el menú.
    """

    if request.method == "POST":
        try:
            # Obtener los datos del formulario
            plato_id = request.POST.get("platoId")
            nombre = request.POST.get("nombrePlato")
            descripcion = request.POST.get("descripcionPlato")
            precio = request.POST.get("precioPlato")
            cantidad = request.POST.get("cantidadPlato")
            imagen = request.POST.get("imagenPlato")

            # Validar que todos los campos sean proporcionados
            if not all([nombre, descripcion, precio, cantidad, imagen]):
                print("⚠️ Faltan datos en la solicitud.")
                return JsonResponse({"status": "error", "message": "Todos los campos son obligatorios"}, status=400)

            # Registrar los datos recibidos en consola
            print(f"📥 Datos recibidos | Nombre: {nombre} | Descripción: {descripcion} | Precio: {precio} | Cantidad: {cantidad} | Imagen: {imagen}")

            if plato_id:
                # 🔹 Actualización de un plato existente
                plato = get_object_or_404(Menu, id=plato_id)
                plato.nombre_plato = nombre
                plato.descripcion = descripcion
                plato.precio = precio
                plato.cantidad_disponible = cantidad
                plato.imagen = imagen
                mensaje = "✅ Plato actualizado correctamente."
                print(f"✏️ Plato ID {plato_id} actualizado: {nombre}")
            else:
                # 🔹 Generar un nuevo ID basado en el total de registros
                nuevo_id = Menu.objects.count() + 1  # SELECT COUNT(*) FROM api_menu + 1
                plato = Menu(
                    id=nuevo_id,  # Asignar ID manualmente
                    nombre_plato=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    cantidad_disponible=cantidad,
                    imagen=imagen
                )
                mensaje = "✅ Plato agregado correctamente."
                print(f"🆕 Nuevo plato agregado ID {nuevo_id}: {nombre}")

            # Guardar en la base de datos
            plato.save()
            return JsonResponse({"status": "success", "message": mensaje})

        except Exception as e:
            print(f"❌ Error al guardar el plato: {str(e)}")
            return JsonResponse({"status": "error", "message": "Ocurrió un error al guardar el plato"}, status=500)

    print("⚠️ Método no permitido en view_guardar_plato.")
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

# 🔹 API para eliminar un plato
@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def view_eliminar_plato(request):
    if request.method == "POST":
        plato_id = request.POST.get("platoId")
        plato = get_object_or_404(Menu, id=plato_id)
        plato.delete()
        return JsonResponse({"status": "success", "message": "Plato eliminado correctamente."})

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)















# ---------------------------------------------
# 🔹 API para realizar una recarga de saldo
@csrf_exempt
@login_required
@user_passes_test(lambda u: u.is_staff)
def api_realizar_recarga(request):
    """Permite a un empleado recargar saldo a un cliente."""
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
    cliente_id = request.POST.get("cliente_id")
    monto = request.POST.get("monto")

    # Validaciones básicas
    if not cliente_id or not monto:
        return JsonResponse({"status": "error", "message": "Cliente y monto son obligatorios"}, status=400)

    try:
        monto_decimal = Decimal(monto)
        if monto_decimal <= 0:
            return JsonResponse({"status": "error", "message": "El monto debe ser mayor a 0"}, status=400)
    except:
        return JsonResponse({"status": "error", "message": "Monto inválido"}, status=400)

    cliente = get_object_or_404(Usuario, id=cliente_id)

    # Registrar la recarga en la base de datos
    nueva_recarga = Recarga(cliente=cliente, empleado=request.user, monto=monto_decimal)
    nueva_recarga.save()

    # Actualizar saldo del cliente
    cliente.saldo += monto_decimal
    cliente.save()

    print(f"✅ Recarga realizada: Cliente {cliente.email} - Monto ${monto_decimal}")

    return JsonResponse({
        "status": "success",
        "message": f"Saldo recargado: ${monto_decimal}",
        "nuevo_saldo": str(cliente.saldo)
    })


# 🔹 API para obtener el historial de recargas
@login_required
def api_historial_recargas(request):
    """Devuelve el historial de recargas, filtrado según el tipo de usuario."""
    if request.user.is_staff:
        recargas = Recarga.objects.all().order_by('-fecha')
    else:
        recargas = Recarga.objects.filter(cliente=request.user).order_by('-fecha')

    historial = [
        {
            "cliente": f"{recarga.cliente.first_name} {recarga.cliente.last_name}",
            "empleado": recarga.empleado.first_name if recarga.empleado else "N/A",
            "monto": str(recarga.monto),
            "fecha": recarga.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for recarga in recargas
    ]

    return JsonResponse({"recargas": historial})


# 🔹 API para obtener la lista de clientes disponibles para recarga
@login_required
@user_passes_test(lambda u: u.is_staff)
def api_lista_clientes(request):
    """Devuelve una lista de clientes para que el empleado pueda seleccionarlos."""
    clientes = Usuario.objects.filter(is_staff=False).values("id", "first_name", "last_name", "email", "saldo")

    return JsonResponse({"clientes": list(clientes)})




# 🔹 API para obtener el historial de pedidos
@login_required
def api_historial_pedidos(request):
    """
    Retorna los pedidos del usuario autenticado.
    - Si es cliente, solo ve sus pedidos.
    - Si es staff, ve todos los pedidos.
    """
    if request.user.is_staff:
        pedidos = Pedido.objects.all().order_by('-fecha')
    else:
        pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')

    historial = [
        {
            "id": pedido.id,
            "cliente": f"{pedido.cliente.first_name} {pedido.cliente.last_name}",
            "fecha": pedido.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "total": str(pedido.total),
            "estado": pedido.estado_pedido,
            "codigo_recogida": pedido.codigo_recogida,
        }
        for pedido in pedidos
    ]

    return JsonResponse({"pedidos": historial})


# 🔹 API para crear un nuevo pedido
@login_required
def api_realizar_pedido(request):
    """
    Permite a un cliente realizar un nuevo pedido.
    Se genera un código de recogida único y se almacena la fecha actual.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    total = request.POST.get("total")

    if not total:
        return JsonResponse({"status": "error", "message": "El total del pedido es obligatorio"}, status=400)

    try:
        total_decimal = Decimal(total)
        if total_decimal <= 0:
            return JsonResponse({"status": "error", "message": "El total debe ser mayor a 0"}, status=400)
    except:
        return JsonResponse({"status": "error", "message": "Total inválido"}, status=400)

    if request.user.saldo < total_decimal:
        return JsonResponse({"status": "error", "message": "Saldo insuficiente"}, status=400)

    # Generar código de recogida único
    codigo_recogida = get_random_string(length=8).upper()

    # Crear el pedido
    nuevo_pedido = Pedido(
        fecha=now(),
        codigo_recogida=codigo_recogida,
        total=total_decimal,
        estado_pedido="Pendiente",
        cliente=request.user
    )
    nuevo_pedido.save()

    # Descontar saldo al cliente
    request.user.saldo -= total_decimal
    request.user.save()

    return JsonResponse({
        "status": "success",
        "message": f"Pedido realizado con éxito. Código de recogida: {codigo_recogida}",
        "codigo_recogida": codigo_recogida
    })


# 🔹 API para cambiar el estado de un pedido (solo administradores)
@login_required
@user_passes_test(lambda u: u.is_staff)
def api_actualizar_estado_pedido(request):
    """Permite a los empleados actualizar el estado de un pedido."""
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    pedido_id = request.POST.get("pedido_id")
    nuevo_estado = request.POST.get("estado")

    if not pedido_id or not nuevo_estado:
        return JsonResponse({"status": "error", "message": "Pedido y estado son obligatorios"}, status=400)

    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado_pedido = nuevo_estado
    pedido.save()

    return JsonResponse({"status": "success", "message": "Estado del pedido actualizado."})



@csrf_exempt
@login_required
def api_realizar_pedido(request):
    """
    Permite a un cliente realizar un nuevo pedido.
    - Se verifica que tenga saldo suficiente.
    - Se genera un código de recogida único.
    - Se descuenta el saldo del usuario.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    data = json.loads(request.body)
    producto_id = data.get("producto_id")
    total = data.get("total")

    if not producto_id or not total:
        return JsonResponse({"status": "error", "message": "Faltan datos en la solicitud"}, status=400)

    try:
        total_decimal = Decimal(total)
        if total_decimal <= 0:
            return JsonResponse({"status": "error", "message": "El total debe ser mayor a 0"}, status=400)
    except:
        return JsonResponse({"status": "error", "message": "Total inválido"}, status=400)

    usuario = request.user

    if usuario.saldo < total_decimal:
        return JsonResponse({"status": "error", "message": "Saldo insuficiente"}, status=400)

    producto = get_object_or_404(Menu, id=producto_id)

    # Generar código de recogida único
    codigo_recogida = get_random_string(length=8).upper()

    # Crear el pedido
    nuevo_pedido = Pedido(
        fecha=now(),
        codigo_recogida=codigo_recogida,
        total=total_decimal,
        estado_pedido="Pendiente",
        cliente=usuario
    )
    nuevo_pedido.save()

    # Descontar saldo al cliente
    usuario.saldo -= total_decimal
    usuario.save()

    return JsonResponse({
        "status": "success",
        "message": f"Pedido realizado con éxito. Código de recogida: {codigo_recogida}",
        "codigo_recogida": codigo_recogida,
        "nuevo_saldo": str(usuario.saldo)
    })


@login_required
def view_dashboard_admin_gestion_balance(request):
    return render(request, "webapp/dashboard_admin/balance.html")



@login_required
@user_passes_test(lambda u: u.is_staff)
def api_consultar_balance(request):
    """Consulta el total de ventas y el detalle de pedidos de un día específico."""
    fecha = request.GET.get("fecha")
    if not fecha:
        return JsonResponse({"status": "error", "message": "⚠ Debes seleccionar una fecha."}, status=400)

    try:
        fecha_consulta = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        pedidos = Pedido.objects.filter(fecha__date=fecha_consulta).order_by("-fecha")

        total_ventas = pedidos.aggregate(Sum("total"))["total__sum"] or 0

        detalle_pedidos = [
            {
                "id": pedido.id,
                "cliente": f"{pedido.cliente.first_name} {pedido.cliente.last_name}",
                "fecha": pedido.fecha.strftime("%d/%m/%Y %H:%M"),
                "total": float(pedido.total),
                "codigo_recogida": pedido.codigo_recogida,
            }
            for pedido in pedidos
        ]

        return JsonResponse({"status": "success", "total_ventas": total_ventas, "pedidos": detalle_pedidos})

    except Exception as e:
        return JsonResponse({"status": "error", "message": f"❌ Error al consultar balance: {e}"}, status=500)

