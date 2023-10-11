from django.db import transaction
from catalogo.models import Plan, Cuota, Viaje

def custom_save(self, *args, **kwargs):
    if self.pago_cliente_estado in ['santander', 'bbva', 'cta-cc €']:
        self.pago_cliente_moneda = 'euro'
    else:
        self.pago_cliente_moneda = 'dolar'

    self.pago_proveedor = round(self.pago_proveedor_precio - (self.pago_proveedor_precio * (self.proveedor.comision / 100)), 2)
    self.ganancia_bruto = self.pago_cliente_monto - self.pago_proveedor
    self.ganancia_usd_vendedor = round(self.pago_cliente_monto * (self.comision_vendedor / 100), 2)
    self.ganancia_gruv = self.ganancia_bruto - self.ganancia_usd_vendedor
    self.ganancia_neta_porc = round((self.ganancia_gruv * 100) / self.ganancia_bruto, 2) if self.ganancia_bruto != 0 else 0

    self.pago_proveedor_moneda = 'dolar'

    ## Crear Plan de pago y Cuotas

    is_cta_cc_payment = self.pago_cliente_estado in ['cta-cc €', 'cta-cc usd']

    # Lógica para calcular el monto_financiado, cantidad_cuotas y monto_por_cuota
    if is_cta_cc_payment and self.pk is None:
        monto_financiado = self.pago_cliente_monto
        fecha_creacion = self.fecha_creacion
        fecha_viaje = self.fecha_viaje
        # Calcular la cantidad de cuotas redondeando hacia abajo
        cantidad_cuotas = (fecha_viaje - fecha_creacion).days // 30
        if cantidad_cuotas < 1:
            cantidad_cuotas = 1
        monto_por_cuota = monto_financiado / cantidad_cuotas

        # Crear el Plan y guardarlo
        with transaction.atomic():
            plan = Plan(
                cliente=self.cliente,
                monto_financiado=monto_financiado,
                cantidad_cuotas=cantidad_cuotas,
                monto_por_cuota=monto_por_cuota
            )
            plan.save()

            # Crear las cuotas asociadas al Plan
            for numero_cuota in range(1, cantidad_cuotas + 1):
                cuota = Cuota(
                    plan=plan,
                    tipo_cuota=self.pago_cliente_estado,
                    monto=monto_por_cuota,
                    numero_cuota=numero_cuota,
                    saldo=round(monto_financiado - numero_cuota * monto_por_cuota, 2),
                    pagado=False
                )
                cuota.save()

    super(Viaje, self).save(*args, **kwargs)