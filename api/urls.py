from django.urls import path

from api import views as api_views

urlpatterns = [
    # 🔹 Rutas de Autenticación
    path("auth/login/", api_views.view_login, name="login"),
    path("auth/logout/", api_views.view_logout, name="logout"),
    path("auth/register/", api_views.view_register, name="register"),

    # 🔹 Rutas del CRUD de Menú
    path("menu/obtener/", api_views.view_obtener_platos, name="obtener_platos"),
    path("menu/guardar/", api_views.view_guardar_plato, name="guardar_plato"),
    path("menu/eliminar/", api_views.view_eliminar_plato, name="eliminar_plato"),
    path("api/realizar/recarga", api_views.api_realizar_recarga, name="api_realizar_recarga"),
    path('api/lista/clientes', api_views.api_lista_clientes, name="api_lista_clientes"),
    path('api/historial/recargas', api_views.api_historial_recargas, name="api_historial_recargas"),
    # Rutas del CRUD de Recargas
    path("pedidos/historial/", api_views.api_historial_pedidos, name="api_historial_pedidos"),
    path("pedidos/realizar/", api_views.api_realizar_pedido, name="api_realizar_pedido"),
    path("pedidos/actualizar_estado/", api_views.api_actualizar_estado_pedido, name="api_actualizar_estado_pedido"),
    path("pedidos/realizar/", api_views.api_realizar_pedido, name="realizar_pedido"),
    path("dashboard/admin/gestion/balance/", api_views.view_dashboard_admin_gestion_balance,
         name="dashboard_admin_gestion_balance"),
    path("api/balance/consultar/", api_views.api_consultar_balance, name="api_consultar_balance"),
]
