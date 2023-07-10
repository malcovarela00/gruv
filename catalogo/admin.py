from django.contrib import admin
from .models import Cliente, Pais, Pago, Proveedor
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('last_login', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

AdminSite.site_header = 'Gruv'
AdminSite.site_title = 'Gruv'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'direccion', 'telefono')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('code_pais', 'nombre')
    search_fields = ('code_pais', 'nombre')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'estado', 'opcion_pago', 'update', 'monto', 'moneda')
    list_filter = ('estado', 'opcion_pago', 'update', 'moneda')
    search_fields = ('cliente__nombre',)
    readonly_fields = ('update',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comision', 'pais', 'update')
    list_filter = ('pais', 'comision', 'update')
    search_fields = ('nombre',)
    readonly_fields = ('update',)
