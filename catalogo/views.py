from django.shortcuts import render
from .models import Viaje, PagoCliente, PagoProveedor, OPCIONES_DE_PAGO
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Sum, F, Case, When, DecimalField

def home(request):
    return render(request, 'home.html')

@staff_member_required
def viaje_list(request):
    viajes_with_saldo = Viaje.objects.select_related('saldo').all()
    return render(request, 'viaje_list.html', {'viajes': viajes_with_saldo})

@staff_member_required
def saldo(request):
    # Obtener todos los pagos de clientes y proveedores
    pagos_cliente = PagoCliente.objects.all()
    pagos_proveedor = PagoProveedor.objects.all()

    # Calcular la suma de las entradas por opciones de pago del cliente
    entradas_por_pago_cliente = pagos_cliente.annotate(
        entrada=Case(
            *[When(opcion_pago=opcion, then=F('monto')) for opcion, _ in OPCIONES_DE_PAGO],
            default=0, output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).values('opcion_pago').annotate(total_entrada=Sum('entrada'))

    # Calcular la suma de las salidas por opciones de pago del proveedor
    salidas_por_pago_proveedor = pagos_proveedor.annotate(
        salida=Case(
            *[When(opcion_pago=opcion, then=F('precio_proveedor')) for opcion, _ in OPCIONES_DE_PAGO],
            default=0, output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).values('opcion_pago').annotate(total_salida=Sum('salida'))

    # Combinar la información de entrada y salida por opción de pago
    saldo_por_pago = []
    for opcion, _ in OPCIONES_DE_PAGO:
        entrada = next((item['total_entrada'] for item in entradas_por_pago_cliente if item['opcion_pago'] == opcion), 0)
        salida = next((item['total_salida'] for item in salidas_por_pago_proveedor if item['opcion_pago'] == opcion), 0)
        saldo = entrada - salida
        saldo_por_pago.append((opcion, entrada, salida, saldo))

    # Renderizar la plantilla con la información calculada
    return render(request, 'saldo.html', {'saldo_por_pago': saldo_por_pago})
