from django.contrib import admin
from .models import Cliente, Pais, Vendedor, Viaje, PagoCliente, Proveedor, PagoProveedor
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('last_login', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

AdminSite.site_header = 'Admin'
AdminSite.site_title = 'Admin'

class PagoClienteInline(admin.TabularInline):
    model = PagoCliente
    extra = 1

class PagoProveedorInline(admin.TabularInline):
    model = PagoProveedor
    extra = 1


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
    list_display = ('nombre', 'apellido', 'email', 'telefono', 'dni')
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    inlines = [PagoClienteInline, PagoProveedorInline]
    list_display = ('cliente', 'producto', 'localizador', 'fecha_viaje', 'fecha_vuelta', 'vendedor', 'comision_vendedor')
    search_fields = ('cliente__nombre', 'producto', 'localizador')
    list_filter = ('fecha_viaje', 'vendedor', )
    readonly_fields = ('update', 'fecha_creacion')


class PagoClienteAdmin(admin.ModelAdmin):
    list_display = ('viaje', 'estado_coloreado', 'opcion_pago', 'monto', 'moneda')
    list_filter = ('estado', 'opcion_pago', 'fecha_vencimiento', 'moneda', 'update', 'fecha_creacion')
    search_fields = ('viaje__producto',)
    readonly_fields = ('update', 'fecha_creacion')

    def estado_coloreado(self, obj):
        if obj.estado == 'confirmado':
            color = 'green' 
        elif obj.estado == 'pendiente':
            color = 'orange'
        else:
            color = 'red'
        return mark_safe(f'<span style="color:{color};">{obj.get_estado_display()}</span>')

    estado_coloreado.short_description = 'Estado'

admin.site.register(PagoCliente, PagoClienteAdmin)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comision', 'pais', 'update')
    list_filter = ('pais', 'comision', 'update')
    search_fields = ('nombre',)
    readonly_fields = ('update',)


@admin.register(PagoProveedor)
class PagoProveedorAdmin(admin.ModelAdmin):
    list_display = ('proveedor', 'estado', 'opcion_pago', 'precio_proveedor', 'moneda', 'update')
    list_filter = ('estado', 'opcion_pago', 'fecha_vencimiento', 'moneda', 'update', 'fecha_creacion')
    search_fields = ('proveedor__nombre',)
    readonly_fields = ('update', 'fecha_creacion')