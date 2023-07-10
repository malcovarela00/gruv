from django.db import models
from .choices import OPCIONES_DE_PAGO, ESTADO, OPCIONES_DE_MODEDA


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Pais(models.Model):
    code_pais = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre + ' (' + self.code_pais + ')'

    class Meta:
        ordering = ['nombre']


class Pago(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO)
    opcion_pago = models.CharField(max_length=10, choices=OPCIONES_DE_PAGO)
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=10, choices=OPCIONES_DE_MODEDA)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cliente.nombre) + ' (' + self.estado + ')'

    class Meta:
        ordering = ['-update']

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    comision = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']