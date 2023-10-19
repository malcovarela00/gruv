from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from .choices import (
    OPCIONES_DE_PAGO,
    OPCIONES_DE_MODEDA,
    OPCIONES_DE_TRANSFERENCIA,
    OPCIONES_DE_TIPO_CUOTA,
    OPCIONES_TIPO_PAGO_PROVEEDOR,
    OPCIONES_MOVIMIENTO,
    TIPO_DE_MOVIMIENTO
)


class Pais(models.Model):
    code_pais = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre + ' (' + self.code_pais + ')'

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    comision = models.DecimalField(max_digits=4, decimal_places=2, default=1, verbose_name='Comision (%)')
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    validado = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


class Viaje(models.Model):
    cliente = models.CharField(max_length=100)
    producto = models.CharField(max_length=200)
    localizador = models.CharField(max_length=50, unique=True)
    pax = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_viaje = models.DateField()
    fecha_vuelta = models.DateField()

    vendedor = models.ForeignKey('Vendedor', on_delete=models.CASCADE)
    comision_vendedor = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Comision Vendedor (%)')

    pago_cliente_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago_cliente_estado = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    pago_cliente_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA, editable=False)
    pago_cliente_fecha_vencimiento = models.DateField()

    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    pago_proveedor_precio = models.DecimalField(max_digits=10, decimal_places=2)
    pago_proveedor_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA, editable=False)
    pago_proveedor_fecha_vencimiento = models.DateField(verbose_name='Fecha de Entrada en Gastos')

    pago_proveedor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    ganancia_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ganancia_usd_vendedor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ganancia_gruv = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ganancia_neta_porc = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    fecha_creacion = models.DateField() #default=timezone.now, editable=False
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cliente} - {self.producto}'

    def save(self, *args, **kwargs):
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

        super(Viaje, self).save(*args, **kwargs)

        if self.pago_cliente_estado not in ['cta-cc €', 'cta-cc usd']:
            # Luego busca y actualiza el objeto Balance, o crea uno nuevo si no existe
            try:
                balance = Balance.objects.get(viaje=self)
                balance.billetera = self.pago_cliente_estado
                balance.movimiento = 'entrada'
                balance.tipo_movimiento = 'pago cliente'
                balance.razon = f'{self.cliente} - {self.producto}'
                balance.monto = self.pago_cliente_monto
                balance.fecha = self.update
                balance.save()
            except Balance.DoesNotExist:
                Balance.objects.create(
                    viaje=self,
                    billetera=self.pago_cliente_estado,
                    movimiento='entrada',
                    tipo_movimiento='pago cliente',
                    razon=f'{self.cliente} - {self.producto}',
                    monto=self.pago_cliente_monto,
                    fecha=self.update
                )

    class Meta:
        ordering = ['-update']


class Transferencia(models.Model):
    salida = models.CharField(max_length=13, choices=OPCIONES_DE_TRANSFERENCIA)
    salida_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entrada = models.CharField(max_length=13, choices=OPCIONES_DE_TRANSFERENCIA)
    entrada_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacion = models.TextField(blank=True,  null=True, verbose_name='Observación')
    
    fecha_creacion = models.DateField() #default=timezone.now, editable=False
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.salida) + ' - ' + str(self.salida_monto)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el objeto PagoProveedor primero

        # Luego busca y actualiza el objeto Balance, o crea uno nuevo si no existe
        balances_salida = Balance.objects.filter(transferencia=self, movimiento='salida')
        for balance_salida in balances_salida:
            balance_salida.billetera = self.salida
            balance_salida.tipo_movimiento = 'transferencia'
            balance_salida.razon = f'Observación: {self.observacion}'
            balance_salida.monto = self.salida_monto
            balance_salida.fecha = self.update
            balance_salida.save()

        # Busca y actualiza los objetos Balance asociados con la entrada de la Transferencia
        balances_entrada = Balance.objects.filter(transferencia=self, movimiento='entrada')
        for balance_entrada in balances_entrada:
            balance_entrada.billetera = self.entrada
            balance_entrada.tipo_movimiento = 'transferencia'
            balance_entrada.razon = f'Observación: {self.observacion}'
            balance_entrada.monto = self.entrada_monto
            balance_entrada.fecha = self.update
            balance_entrada.save()
        # Si no se encontraron objetos Balance, crea nuevos objetos
        if not balances_salida.exists():
            Balance.objects.create(
                transferencia=self,
                billetera=self.salida,
                movimiento='salida',
                tipo_movimiento='transferencia',
                razon=f'Observación: {self.observacion}',
                monto=self.salida_monto,
                fecha=self.update
            )
        if not balances_entrada.exists():
            Balance.objects.create(
                transferencia=self,
                billetera=self.entrada,
                movimiento='entrada',
                tipo_movimiento='transferencia',
                razon=f'Observación: {self.observacion}',
                monto=self.entrada_monto,
                fecha=self.update
            )

    class Meta:
        ordering = ['-update']


class PagoProveedor(models.Model):
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=13, choices=OPCIONES_TIPO_PAGO_PROVEEDOR, verbose_name='Tipo de Pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacion = models.TextField(blank=True,  null=True, verbose_name='Observación')

    fecha_creacion = models.DateField() #default=timezone.now, editable=False
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pais) + ' - ' + str(self.monto)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el objeto PagoProveedor primero

    # Luego busca y actualiza el objeto Balance, o crea uno nuevo si no existe
        try:
            balance = Balance.objects.get(pago_proveedor=self)
            balance.billetera = self.tipo_pago
            balance.movimiento = 'salida'
            balance.tipo_movimiento = 'pago proveedor'
            balance.razon = f'{self.pais}'
            balance.monto = self.monto
            balance.fecha = self.update
            balance.save()
        except Balance.DoesNotExist:
            Balance.objects.create(
                pago_proveedor=self,
                billetera=self.tipo_pago,
                movimiento='salida',
                tipo_movimiento='pago proveedor',
                razon=f'{self.pais}',
                monto=self.monto,
                fecha=self.update
            )

    class Meta:
        ordering = ['-update']
        verbose_name = 'Pago Proveedor'
        verbose_name_plural = 'Pago Proveedores'


class Plan(models.Model):
    cliente = models.CharField(max_length=100)
    monto_financiado = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Monto a Financiar')
    cantidad_cuotas = models.PositiveSmallIntegerField(verbose_name='Cantidad de Cuotas')
    monto_por_cuota = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Monto por Cuota')

    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cliente) + ' - ' + str(self.monto_financiado)

    class Meta:
        ordering = ['-update']
        verbose_name = 'Plan de Pago'
        verbose_name_plural = 'Plan de Pagos'


class Cuota(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    tipo_cuota = models.CharField(max_length=13, choices=OPCIONES_DE_TIPO_CUOTA)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_cuota = models.PositiveSmallIntegerField(verbose_name='Número de Cuota')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.BooleanField(default=False)
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')

    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.plan) + ' - ' + str(self.numero_cuota)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el objeto PagoProveedor primero

        # Luego busca y actualiza el objeto Balance, o crea uno nuevo si no existe
        if self.pagado:
            try:
                balance = Balance.objects.get(cuota=self)
                balance.billetera = self.tipo_cuota
                balance.movimiento = 'entrada'
                balance.tipo_movimiento = 'cuota'
                balance.razon = f'{self.plan} - {self.numero_cuota}'
                balance.monto = self.monto
                balance.fecha = self.update
                balance.save()
            except Balance.DoesNotExist:
                Balance.objects.create(
                    cuota=self,
                    billetera=self.tipo_cuota,
                    movimiento='entrada',
                    tipo_movimiento='cuota',
                    razon=f'{self.plan} - {self.numero_cuota}',
                    monto=self.monto,
                    fecha=self.update
                )

    class Meta:
        ordering = ['numero_cuota']


class Balance(models.Model):
    viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE, blank=True, null=True)
    transferencia = models.ForeignKey('Transferencia', on_delete=models.CASCADE, blank=True, null=True)
    pago_proveedor = models.ForeignKey('PagoProveedor', on_delete=models.CASCADE, blank=True, null=True)
    cuota = models.ForeignKey('Cuota', on_delete=models.CASCADE, blank=True, null=True)
    
    billetera = models.CharField(max_length=20, choices=OPCIONES_DE_PAGO)
    movimiento = models.CharField(max_length=20,choices=OPCIONES_MOVIMIENTO)
    tipo_movimiento = models.CharField(max_length=100, choices=TIPO_DE_MOVIMIENTO)
    razon = models.CharField(max_length=100, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        return f'{self.billetera} - {self.movimiento} - {self.tipo_movimiento} - {self.razon} - {self.monto}'