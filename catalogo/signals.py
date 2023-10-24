from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from catalogo.models import Viaje, Plan, Cuota

@receiver(post_save, sender=Viaje)
def create_plan_and_cuotas(sender, instance, created, **kwargs):
    is_cta_cc_payment = instance.pago_cliente_estado in ['cta-cc €', 'cta-cc usd']

    if is_cta_cc_payment and created:
        if instance.pago_cliente_moneda == 'euro':
            tipo_cuota_plan = 'santander'
        else:
            tipo_cuota_plan = 'usdt'

        monto_financiado = instance.pago_cliente_monto
        fecha_creacion = instance.fecha_creacion
        fecha_viaje = instance.fecha_viaje
        cantidad_cuotas = (fecha_viaje - fecha_creacion).days // 30
        if cantidad_cuotas < 1:
            cantidad_cuotas = 1
        monto_por_cuota = monto_financiado / cantidad_cuotas

        # Crear el Plan y guardarlo
        with transaction.atomic():
            plan = Plan(
                cliente=instance.cliente,
                monto_financiado=monto_financiado,
                cantidad_cuotas=cantidad_cuotas,
                monto_por_cuota=monto_por_cuota,
                cuenta_corriente=instance.pago_cliente_estado
            )
            plan.save()

            # Crear las cuotas asociadas al Plan
            for numero_cuota in range(cantidad_cuotas, 0, -1):
                cuota = Cuota(
                    plan=plan,
                    tipo_cuota=tipo_cuota_plan,
                    monto=monto_por_cuota,
                    numero_cuota=numero_cuota,
                    saldo=round(monto_financiado - numero_cuota * monto_por_cuota, 2),
                    pagado=False,
                    fecha_vencimiento=fecha_creacion
                )
                cuota.save()