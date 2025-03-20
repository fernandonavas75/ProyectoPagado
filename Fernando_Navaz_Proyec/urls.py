"""Fernando_Navaz_Proyec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from webapp import views as webapp_views
from api import views as api_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path('', webapp_views.view_index, name='index'),
    # Paths para el dashboard

    path('dashboard/usuarios/', webapp_views.view_dashboard_usuarios, name='dashboard_usuarios'),
    path('dashboard/admin/',webapp_views.view_dashboard_admin,name='dashboard_admin'),
    path('dashboard/admin/gestion/menu/',webapp_views.view_dashboard_admin_gestion_menu,name='dashboard_admin_gestion_menu'),
    path('dashboard/admin/gestion/menu/editar/<int:producto_id>/',
         webapp_views.view_dashboard_admin_menu_editar,
         name='dashboard_admin_gestion_menu_editar'),

    path('dashboard/admin/gestion/menu/agregar/', webapp_views.view_dashboard_admin_menu_agregar,
         name='dashboard_admin_gestion_menu_agregar'),

    path('dashboard/admin/gestion/recargas/',webapp_views.view_dashboard_admin_gestion_recargas,name='dashboard_admin_gestion_recargas'),
    path('dashboard/admin/gestion/balance/', webapp_views.view_dashboard_admin_gestion_balance,name='dashboard_admin_gestion_balance'),
    path('dashboard/admin/gestion/pedidos/',webapp_views.view_dashboard_admin_gestion_pedidos,name='dashboard_admin_gestion_pedidos'),
    path('dashboard/admin/gestion/usuarios',webapp_views.view_dashboard_admin_gestion_usuarios,name='dashboard_admin_gestion_usuarios'),
    path("dashboard/admin/gestion/usuarios/editar/<int:usuario_id>/", webapp_views.view_dashboard_admin_gestion_usuarios_editar, name="dashboard_admin_gestion_usuarios_editar"),
    path("dashboard/admin/gestion/usuarios/eliminar/<int:usuario_id>/", webapp_views.view_dashboard_admin_gestion_usuarios_eliminar, name="dashboard_admin_gestion_usuarios_eliminar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)