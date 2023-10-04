from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from .choices import OPCIONES_DE_PAGO, ESTADO, OPCIONES_DE_MODEDA


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
    comision = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
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


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Viaje(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    localizador = models.CharField(max_length=50, unique=True)
    pax = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_viaje = models.DateField()
    fecha_vuelta = models.DateField()

    vendedor = models.ForeignKey('Vendedor', on_delete=models.CASCADE)
    comision_vendedor = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, validators=[MinValueValidator(0)], verbose_name='Comision Vendedor (%)')

    pago_cliente_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pago_cliente_estado = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    pago_cliente_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA, editable=False)
    pago_cliente_fecha_vencimiento = models.DateField()

    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    pago_proveedor_estado = models.CharField(max_length=10, choices=ESTADO)
    pago_proveedor_precio = models.DecimalField(max_digits=10, decimal_places=2)
    pago_proveedor_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA, editable=False)
    pago_proveedor_fecha_vencimiento = models.DateField(verbose_name='Fecha de Entrada en Gastos')

    pago_proveedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    ganancia_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_usd_vendedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_gruv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_neta_porc = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
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

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-update']


class Transferencia(models.Model):
    sale = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    sale_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    entra = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    entra_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacion = models.CharField(max_length=300, blank=True, null=True, verbose_name='Observación')
    
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sale

    class Meta:
        ordering = ['-update']
