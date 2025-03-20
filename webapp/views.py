from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from api.models import Menu, Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  # ✅ Importamos messages para notificaciones
# Create your views here.


def view_index(request):
    return render(request, 'webapp/index.html')


@login_required
def view_dashboard_usuarios(request):
    usuario = request.user
    nombre_usuario = f'{str(usuario.first_name)} {str(usuario.last_name)}'
    saldo = usuario.saldo
    productos = Menu.objects.all()
    # print(f'Datos del usuario: Nombre |{nombre_usuario}|, saldo: |{saldo}|, productos: {productos}')

    return render(request, "webapp/dashboard_usuarios/cliente.html", {
        "saldo": saldo,
        "productos": productos,
        "nombre_usuario": nombre_usuario,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email

    return render(request, "webapp/dashboard_admin/admin.html", {
        "nombre_usuario": nombre_usuario
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_menu(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    menu = Menu.objects.all()
    return render(request, 'webapp/dashboard_admin/menu.html',
                  {"nombre_usuario": nombre_usuario,
                   "productos": menu
                   })


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_menu_agregar(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email

    if request.method == "POST":
        nombre = request.POST.get("nombrePlato")
        descripcion = request.POST.get("descripcionPlato")
        precio = request.POST.get("precioPlato")
        cantidad = request.POST.get("cantidadPlato")
        imagen = request.POST.get("imagenPlato")

        # 🖨️ Imprimir datos recibidos para depuración
        print(
            f"📥 Recibiendo datos del formulario: Nombre: {nombre}, Descripción: {descripcion}, Precio: {precio}, Cantidad: {cantidad}, Imagen: {imagen}")

        # ✅ Validar que los campos no estén vacíos
        if not nombre or not descripcion or not precio or not cantidad or not imagen:
            print("❌ Error: Campos vacíos detectados.")
            messages.error(request, "Todos los campos son obligatorios.")  # ✅ Mensaje flotante de error
            return redirect('dashboard_admin_gestion_menu_agregar')

        try:
            # ✅ Crear nuevo producto
            nuevo_plato = Menu(
                nombre_plato=nombre,
                descripcion=descripcion,
                precio=float(precio),
                cantidad_disponible=int(cantidad),
                imagen=imagen
            )
            nuevo_plato.save()

            print(f"✅ Producto agregado con éxito: ID {nuevo_plato.id}, Nombre {nuevo_plato.nombre_plato}")
            messages.success(request, "Producto agregado correctamente.")  # ✅ Mensaje flotante de éxito
            return redirect('dashboard_admin_gestion_menu')  # ✅ Redirección correcta

        except Exception as e:
            print(f"❌ Error al guardar el producto: {e}")
            messages.error(request, "Error al guardar el producto.")  # ✅ Mensaje flotante de error
            return redirect('dashboard_admin_gestion_menu_agregar')

    return render(request, 'webapp/dashboard_admin/crud_menu/menu_agregar.html', {"nombre_usuario": nombre_usuario})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_menu_editar(request, producto_id):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email

    # 🔎 Buscar el producto por ID
    producto = get_object_or_404(Menu, id=producto_id)

    if request.method == "POST":
        nombre = request.POST.get("nombrePlato")
        descripcion = request.POST.get("descripcionPlato")
        precio = request.POST.get("precioPlato")
        cantidad = request.POST.get("cantidadPlato")
        imagen = request.POST.get("imagenPlato")

        print(f"📥 Editando producto: ID {producto.id}, Nombre: {nombre}, Descripción: {descripcion}, Precio: {precio}, Cantidad: {cantidad}, Imagen: {imagen}")

        if not nombre or not descripcion or not precio or not cantidad or not imagen:
            print("❌ Error: Campos vacíos detectados.")
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('dashboard_admin_gestion_menu_editar', producto_id=producto.id)

        try:
            producto.nombre_plato = nombre
            producto.descripcion = descripcion
            producto.precio = float(precio)
            producto.cantidad_disponible = int(cantidad)
            producto.imagen = imagen
            producto.save()

            print(f"✅ Producto actualizado con éxito: ID {producto.id}, Nombre {producto.nombre_plato}")
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('dashboard_admin_gestion_menu')

        except Exception as e:
            print(f"❌ Error al actualizar el producto: {e}")
            messages.error(request, "Error al actualizar el producto.")
            return redirect('dashboard_admin_gestion_menu_editar', producto_id=producto.id)

    return render(request, 'webapp/dashboard_admin/crud_menu/menu_editar.html',
                  {"nombre_usuario": nombre_usuario, "producto": producto})



@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_recargas(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    return render(request, 'webapp/dashboard_admin/recargas.html', {"nombre_usuario": nombre_usuario})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_balance(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    return render(request, 'webapp/dashboard_admin/balance.html', {"nombre_usuario": nombre_usuario})


@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_pedidos(request):
    usuario = request.user
    nombre_usuario = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.email
    return render(request, 'webapp/dashboard_admin/pedidos.html', {"nombre_usuario": nombre_usuario})



@login_required
@user_passes_test(lambda u: u.is_staff)
def view_dashboard_admin_gestion_usuarios(request):
    usuario_admin = request.user
    nombre_usuario = f"{usuario_admin.first_name} {usuario_admin.last_name}".strip() or usuario_admin.email

    usuarios = Usuario.objects.all()

    # Depuración
    if not usuarios.exists():
        print("❌ No hay usuarios en la base de datos.")
    else:
        for user in usuarios:
            print(f"✔ Usuario encontrado: {user.first_name} {user.last_name} - {user.email}")

    return render(request, "webapp/dashboard_admin/usuarios.html", {"usuarios": usuarios, "nombre_usuario": nombre_usuario})

@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo administradores pueden acceder
def view_dashboard_admin_gestion_usuarios_editar(request, usuario_id):
    usuario_admin = request.user
    nombre_usuario = f"{usuario_admin.first_name} {usuario_admin.last_name}".strip() or usuario_admin.email

    usuario = get_object_or_404(Usuario, id=usuario_id)  # ⚠️ Eliminamos el filtro is_staff=False

    if request.method == "POST":
        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")
        usuario.email = request.POST.get("email")
        usuario.saldo = request.POST.get("saldo")
        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("/dashboard/admin/gestion/usuarios")  # Redirección fija

    print(usuario)
    return render(request, "webapp/dashboard_admin/usuarios_editar.html", {"usuario": usuario, "nombre_usuario": nombre_usuario,})



@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo administradores pueden acceder
def view_dashboard_admin_gestion_usuarios_eliminar(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id, is_staff=False)
    usuario.delete()
    messages.success(request, "Usuario eliminado correctamente.")
    return redirect("dashboard_admin_gestion_usuarios")