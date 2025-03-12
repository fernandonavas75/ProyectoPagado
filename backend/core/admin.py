from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Usuario, Menu, Pedido, DetallePedido, Recarga, Balance

admin.site.register(Usuario)
admin.site.register(Menu)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Recarga)
admin.site.register(Balance)
