from rest_framework.permissions import BasePermission

class EsEmpleado(BasePermission):
    """
    Permiso para permitir acceso solo a empleados.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'empleado'
