from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Viaje, PagoProveedor, PagoCliente, Saldo


@receiver(post_save, sender=Viaje)
def create_or_update_saldo(sender, instance, created, **kwargs):
    try:
        saldo = Saldo.objects.get(viaje=instance)
    except Saldo.DoesNotExist:
        saldo = Saldo(viaje=instance)

    # Retrieve related objects
    pago_proveedor = instance.pagoproveedor
    pago_cliente = instance.pagocliente

    # Update fields in Saldo
    saldo.pago_cliente_estado = pago_cliente.estado
    saldo.pago_cliente_opcion_pago = pago_cliente.opcion_pago
    saldo.pago_cliente_monto = pago_cliente.monto
    saldo.pago_cliente_moneda = pago_cliente.moneda

    saldo.pago_proveedor_estado = pago_proveedor.estado
    saldo.pago_proveedor_opcion_pago = pago_proveedor.opcion_pago
    saldo.pago_proveedor_precio = pago_proveedor.precio_proveedor
    saldo.pago_proveedor_moneda = pago_proveedor.moneda
    saldo.pago_proveedor = round(saldo.pago_proveedor_precio - (saldo.pago_proveedor_precio * (pago_proveedor.proveedor.comision / 100)), 2)

    saldo.ganancia_bruto = pago_cliente.monto - saldo.pago_proveedor
    saldo.ganancia_usd_vendedor = round(pago_cliente.monto * (instance.comision_vendedor / 100), 2)
    saldo.ganancia_gruv = saldo.ganancia_bruto - saldo.ganancia_usd_vendedor
    saldo.ganancia_neta_porc = round((saldo.ganancia_gruv * 100) / saldo.ganancia_bruto, 2) if saldo.ganancia_bruto != 0 else 0
    

    saldo.save()

@receiver(post_save, sender=PagoCliente)
def update_saldo_on_pagocliente_save(sender, instance, created, **kwargs):
    if created:
        # PagoCliente instance is created, update related Saldo
        saldo, _ = Saldo.objects.get_or_create(viaje=instance.viaje)
    else:
        # PagoCliente instance is updated, update related Saldo
        saldo = Saldo.objects.get(viaje=instance.viaje)

    # Update fields in Saldo based on PagoCliente
    saldo.pago_cliente_estado = instance.estado
    saldo.pago_cliente_opcion_pago = instance.opcion_pago
    saldo.pago_cliente_monto = instance.monto
    saldo.pago_cliente_moneda = instance.moneda
    saldo.pago_proveedor = round(saldo.pago_proveedor_precio - (saldo.pago_proveedor_precio * (instance.viaje.pagoproveedor.proveedor.comision / 100)), 2)
    
    saldo.ganancia_bruto = instance.monto - saldo.pago_proveedor
    saldo.ganancia_usd_vendedor = round(instance.monto * (instance.viaje.comision_vendedor / 100), 2)
    saldo.ganancia_gruv = saldo.ganancia_bruto - saldo.ganancia_usd_vendedor
    saldo.ganancia_neta_porc = round((saldo.ganancia_gruv * 100) / saldo.ganancia_bruto, 2) if saldo.ganancia_bruto != 0 else 0

    saldo.save()


@receiver(post_save, sender=PagoProveedor)
def update_saldo_on_pagoproveedor_save(sender, instance, created, **kwargs):
    if created:
        # PagoProveedor instance is created, update related Saldo
        saldo, _ = Saldo.objects.get_or_create(viaje=instance.viaje)
    else:
        # PagoProveedor instance is updated, update related Saldo
        saldo = Saldo.objects.get(viaje=instance.viaje)

    # Update fields in Saldo based on PagoProveedor
    saldo.pago_proveedor_estado = instance.estado
    saldo.pago_proveedor_opcion_pago = instance.opcion_pago
    saldo.pago_proveedor_precio = instance.precio_proveedor
    saldo.pago_proveedor_moneda = instance.moneda
    saldo.pago_proveedor = round(instance.precio_proveedor - (instance.precio_proveedor * (instance.proveedor.comision / 100)), 2)
    
    saldo.ganancia_bruto = saldo.pago_cliente_monto - instance.precio_proveedor
    saldo.ganancia_usd_vendedor = round(instance.viaje.pagocliente.monto * (instance.viaje.comision_vendedor / 100), 2)
    saldo.ganancia_gruv = saldo.ganancia_bruto - saldo.ganancia_usd_vendedor
    saldo.ganancia_neta_porc = round((saldo.ganancia_gruv * 100) / saldo.ganancia_bruto, 2) if saldo.ganancia_bruto != 0 else 0

    saldo.save()
