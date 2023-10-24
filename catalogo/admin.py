from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from .models import (
    Pais,
    Proveedor,
    Vendedor,
    Viaje,
    Transferencia,
    OpcionPago,
    Cuota,
    Pago,
    Plan,
    Balance,
)


class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('last_login', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

AdminSite.site_header = 'Admin'
AdminSite.site_title = 'Admin'


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('code_pais', 'nombre')
    fields = [('code_pais', 'nombre')]
    search_fields = ('code_pais', 'nombre')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comision', 'pais', 'update')
    fields = ['nombre', ('comision', 'pais')]
    list_filter = ('pais', 'update')
    search_fields = ('nombre',)
    readonly_fields = ('update',)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'telefono')
    fields = [('nombre', 'apellido'), ('email', 'telefono')]
    search_fields = ('nombre', 'apellido', 'email', 'telefono')
    list_filter = ('pais', 'update')
    readonly_fields = ('update',)


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'producto', 'localizador', 'fecha_viaje', 'pago_cliente_monto', 'vendedor')
    fields = [('cliente', 'dni'), ('pax', 'producto', 'localizador'), ('fecha_viaje', 'fecha_vuelta'), 
              ('vendedor', 'comision_vendedor'), ('pago_cliente_monto', 'pago_cliente_estado', 'pago_cliente_fecha_vencimiento'),
              ('proveedor', 'pago_proveedor_web', 'pago_proveedor_fecha_vencimiento', 'fecha_creacion'),
              ('pago_proveedor', 'ganancia_bruto', 'ganancia_usd_vendedor', 'ganancia_gruv', 'ganancia_neta_porc')]
    search_fields = ('cliente', 'producto', 'localizador')
    list_filter = ('fecha_viaje', 'pax', 'proveedor', 'pago_cliente_estado', 'fecha_creacion')
    readonly_fields = ('update', 'pago_proveedor','ganancia_bruto', 'ganancia_usd_vendedor', 'ganancia_gruv', 'ganancia_neta_porc') #'fecha_creacion'


@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('salida', 'salida_monto', 'entrada', 'entrada_monto')
    fields = [('salida', 'salida_monto'), ('entrada', 'entrada_monto'), ('observacion', 'fecha_creacion')]
    search_fields = ('salida', 'entrada', 'observacion')
    list_filter = ('salida_monto', 'entrada_monto')
    readonly_fields = ('update',)


@admin.register(OpcionPago)
class OpcionPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    readonly_fields = ('update',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pago_proveedor', 'otros_pagos', 'tipo_pago', 'monto')
    fields = [('pago_proveedor', 'otros_pagos'), ('tipo_pago', 'monto',), ('observacion', 'fecha_creacion')]
    search_fields = ('pago_proveedor__nombre', 'otros_pagos__nombre', 'tipo_pago')
    list_filter = ('pago_proveedor', 'otros_pagos', 'fecha_creacion')
    readonly_fields = ('update',)

class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'monto_financiado', 'cantidad_cuotas', 'monto_por_cuota', 'fecha_creacion')
    fields = [('cliente', 'cuenta_corriente'), ('monto_financiado', 'cantidad_cuotas', 'monto_por_cuota')]
    list_filter = ('fecha_creacion', 'cantidad_cuotas')
    search_fields = ('cliente',)
    inlines = [CuotaInline]

@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ('plan', 'tipo_cuota', 'monto', 'numero_cuota', 'saldo', 'fecha_creacion', 'pagado')
    fields = [('plan', 'tipo_cuota'), ('monto', 'numero_cuota', 'saldo','fecha_vencimiento'), 'pagado']
    list_filter = ('pagado', 'numero_cuota',)
    search_fields = ('plan__cliente',)


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('billetera', 'movimiento', 'tipo_movimiento', 'razon', 'monto', 'fecha')
    fields = [('viaje', 'transferencia', 'pago_proveedor', 'cuota'), ('billetera', 'movimiento'), ('tipo_movimiento', 'razon', 'monto','fecha')]
    list_filter = ('billetera', 'movimiento', 'fecha')
    search_fields = ('billetera', 'movimiento', 'tipo_movimiento')