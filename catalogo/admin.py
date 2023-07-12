from django.contrib import admin
from .models import Cliente, Pais, Vendedor, Viaje, PagoCliente, Proveedor, ViajeProveedor, PagoProveedor
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('last_login', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

AdminSite.site_header = 'Gruv'
AdminSite.site_title = 'Gruv'


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('code_pais', 'nombre')
    search_fields = ('code_pais', 'nombre')


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'direccion', 'telefono', 'dni')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'localizador', 'fecha_viaje', 'fecha_vuelta', 'vendedor')
    search_fields = ('cliente', 'producto', 'localizador')
    list_filter = ('fecha_viaje', 'vendedor')
    readonly_fields = ('update',)


@admin.register(PagoCliente)
class PagoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'estado', 'opcion_pago', 'viaje', 'monto', 'comision_vendedor', 'moneda')
    list_filter = ('estado', 'opcion_pago', 'fecha_vencimiento', 'moneda', 'update')
    search_fields = ('cliente__nombre', 'viaje')
    readonly_fields = ('update',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comision', 'pais', 'update')
    list_filter = ('pais', 'comision', 'update')
    search_fields = ('nombre',)
    readonly_fields = ('update',)


@admin.register(ViajeProveedor)
class ViajeProveedorAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'proveedor')
    list_filter = ('proveedor', 'update')
    search_fields = ('viaje', 'proveedor')
    readonly_fields = ('update',)


@admin.register(PagoProveedor)
class PagoProveedorAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'estado', 'opcion_pago', 'update', 'monto', 'moneda')
    list_filter = ('estado', 'opcion_pago', 'fecha_vencimiento', 'moneda', 'update')
    search_fields = ('proveedor__nombre',)
    readonly_fields = ('update',)