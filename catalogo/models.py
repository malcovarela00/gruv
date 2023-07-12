from django.db import models
from .choices import OPCIONES_DE_PAGO, ESTADO, OPCIONES_DE_MODEDA


class Pais(models.Model):
    code_pais = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre + ' (' + self.code_pais + ')'

    class Meta:
        ordering = ['nombre']

    class Meta:
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
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def dni_upper(self):
        return self.dni.upper()
    dni_upper.short_description = 'DNI'

    class Meta:
        ordering = ['nombre']


class Viaje(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    localizador = models.CharField(max_length=50)
    pax = models.PositiveSmallIntegerField(blank=True, null=True)
    fecha_viaje = models.DateField(blank=True, null=True)
    fecha_vuelta = models.DateField(blank=True, null=True)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.producto


class PagoCliente(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    opcion_pago = models.CharField(max_length=10, choices=OPCIONES_DE_PAGO)
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    comision_vendedor = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    fecha_vencimiento = models.DateField()
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cliente.nombre) + ' (' + self.estado + ')'

    class Meta:
        ordering = ['-update']
        verbose_name = 'Pago-Cliente'
        verbose_name_plural = 'Pagos-Clientes'


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    comision = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'


class ViajeProveedor(models.Model):
    viaje = models.ForeignKey('Viaje', on_delete=models.CASCADE)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.viaje} - {self.proveedor}'

    class Meta:
        verbose_name = 'Viaje-Proveedor'
        verbose_name_plural = 'Viaje-Proveedores'


class PagoProveedor(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    opcion_pago = models.CharField(max_length=10, choices=OPCIONES_DE_PAGO)
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    fecha_vencimiento = models.DateField()
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.proveedor.nombre) + ' (' + self.estado + ')'

    class Meta:
        ordering = ['-update']
        verbose_name = 'Pago-Proveedor'
        verbose_name_plural = 'Pagos-Proveedores'