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

    saldo.pago_proveedor = saldo.pago_proveedor_precio - (saldo.pago_proveedor_precio * (pago_proveedor.proveedor.comision / 100))
    saldo.ganancia_bruto = pago_cliente.monto - saldo.pago_proveedor

    saldo.save()
