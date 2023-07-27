from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError
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
    dni = models.CharField(max_length=20, unique=True, verbose_name='DNI/Pasaporte/ID')
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
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto

    def clean(self):
        super(Viaje, self).clean()

        if self.fecha_vuelta is not None and self.fecha_viaje is not None:
            if self.fecha_vuelta < self.fecha_viaje:
                raise ValidationError("La Fecha de Vuelta debe ser posterior a la Fecha de Viaje.")


class PagoCliente(models.Model):
    viaje = models.OneToOneField('Viaje', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    opcion_pago = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    fecha_vencimiento = models.DateField()
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.viaje) + ' (' + self.estado + ')'

    def save(self, *args, **kwargs):
        if self.opcion_pago == 'usdt':
            self.moneda = 'dolar'
        else:
            self.moneda = 'euro'
        super().save(*args, **kwargs)

    def clean(self):
        super(PagoCliente, self).clean()

        if self.fecha_vencimiento < timezone.localdate():
            raise ValidationError("La Fecha de Vencimiento: debe ser posterior a la fecha de hoy.")

    class Meta:
        ordering = ['-update']
        verbose_name = 'Pago Cliente'
        verbose_name_plural = 'Pagos Clientes'


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


class PagoProveedor(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    viaje = models.OneToOneField('Viaje', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    opcion_pago = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    precio_proveedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Entrada en Gastos')
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.proveedor.nombre) + ' (' + self.estado + ')'

    def save(self, *args, **kwargs):
        if self.opcion_pago == 'santander':
            self.moneda = 'euro'
        else:
            self.moneda = 'dolar'
        super().save(*args, **kwargs)

    def clean(self):
        super(PagoProveedor, self).clean()

        if self.fecha_vencimiento < timezone.localdate():
            raise ValidationError("La Fecha de Entrada en Gastos: debe ser posterior a la fecha de hoy.")

    class Meta:
        ordering = ['-update']
        verbose_name = 'Pago Proveedor'
        verbose_name_plural = 'Pagos Proveedores'


class Saldo(models.Model):
    viaje = models.OneToOneField('Viaje', on_delete=models.CASCADE)
    
    pago_cliente_monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pago_cliente_estado = models.CharField(max_length=10, choices=ESTADO)
    pago_cliente_opcion_pago = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    pago_cliente_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    
    pago_proveedor_estado = models.CharField(max_length=10, choices=ESTADO)
    pago_proveedor_opcion_pago = models.CharField(max_length=13, choices=OPCIONES_DE_PAGO)
    pago_proveedor_precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pago_proveedor_moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    pago_proveedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    
    ganancia_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_usd_vendedor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_gruv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    ganancia_neta_porc = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    def __str__(self):
        return f"Saldo para {self.viaje}"
