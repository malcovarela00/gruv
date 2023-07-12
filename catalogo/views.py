from django.shortcuts import render
from .models import Pago, Viaje, Proveedor
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'home.html')

@staff_member_required
def tabla_pagos(request):
    pagos = Pago.objects.select_related('cliente').all()
    datos = []
    for pago in pagos:
        viaje = Viaje.objects.filter(cliente=pago.cliente).first()
        if viaje:
            proveedor = Proveedor.objects.filter(viajeproveedor__viaje=viaje).first()
            datos.append({
                'estado': pago.estado,
                'localizador': viaje.localizador,
                'producto': viaje.producto,
                'fecha_viaje': viaje.fecha_viaje,
                'fecha_vuelta': viaje.fecha_vuelta,
                'nombre_cliente': pago.cliente.nombre,
                'pax': viaje.pax,
                'pais_proveedor': proveedor.pais.nombre if proveedor else '',
                'nombre_proveedor': proveedor.nombre if proveedor else '',
                'monto_pago': pago.monto,
                'vendedor': viaje.vendedor.username
            })
    return render(request, 'tabla_pagos.html', {'datos': datos})

