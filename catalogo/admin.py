from django.contrib import admin
from .models import Pais, Proveedor, Vendedor, Cliente, Viaje, Transferencia
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User



class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('last_login', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

AdminSite.site_header = 'Admin'
AdminSite.site_title = 'Admin'


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('code_pais', 'nombre')
    search_fields = ('code_pais', 'nombre')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comision', 'pais', 'update')
    list_filter = ('pais', 'update')
    search_fields = ('nombre',)
    readonly_fields = ('update',)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'localizador', 'fecha_viaje', 'pago_cliente_monto', 'vendedor')
    fields = [('cliente', 'pax'), ('producto', 'localizador'), ('fecha_viaje', 'fecha_vuelta'), 
              ('vendedor', 'comision_vendedor'), ('pago_cliente_monto', 'pago_cliente_estado', 'pago_cliente_fecha_vencimiento'),
              ('proveedor', 'pago_proveedor_estado', 'pago_proveedor_precio'), 'pago_proveedor_fecha_vencimiento',]
    search_fields = ('cliente__nombre', 'producto', 'localizador')
    list_filter = ('fecha_viaje', 'proveedor__nombre', 'pax', 'proveedor', 'update')
    readonly_fields = ('update', 'fecha_creacion')


@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('sale', 'sale_monto', 'entra', 'entra_monto')
    fields = [('sale', 'sale_monto'), ('entra', 'entra_monto'), 'observacion']
    search_fields = ('sale', 'entra', 'observacion')
    list_filter = ('sale_monto', 'entra_monto')
    readonly_fields = ('update',)


