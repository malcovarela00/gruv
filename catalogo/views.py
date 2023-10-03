from django.shortcuts import render
from .models import Viaje, Proveedor, OPCIONES_DE_PAGO
from django.contrib.admin.views.decorators import staff_member_required

from decimal import Decimal
from datetime import datetime
from django.utils import timezone

from django.db.models import Sum, F, Case, When, DecimalField
from django.views.generic import TemplateView

def home(request):
    return render(request, 'home.html')

@staff_member_required
def viaje_list(request):
    viajes = Viaje.objects.all()
    return render(request, 'viaje_list.html', {'viajes': viajes})

# @staff_member_required
# def balance(request):

#     if request.method == 'GET':
#         # Valores predeterminados para las fechas
#         start_date = datetime.now().date()
#         end_date = datetime.now().date()
        
#         # Obtener las fechas del formulario si se proporcionan
#         start_date_str = request.GET.get('start_date', start_date.strftime('%Y-%m-%d'))
#         end_date_str = request.GET.get('end_date', end_date.strftime('%Y-%m-%d'))

#         # Convertir las fechas a objetos datetime.date
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#         # Convertir las fechas a objetos datetime con zona horaria
#         start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
#         end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

#     # Filtrar los pagos de clientes y proveedores por rango de fechas
#         pagos_cliente = PagoCliente.objects.filter(fecha_creacion__gte=start_datetime, fecha_creacion__lte=end_datetime)
#         pagos_proveedor = PagoProveedor.objects.filter(fecha_creacion__gte=start_datetime, fecha_creacion__lte=end_datetime)
#     else:
#         pagos_cliente = PagoCliente.objects.all()
#         pagos_proveedor = PagoProveedor.objects.all()

#     # Calcular la suma de las entradas por opciones de pago del cliente
#     entradas_por_pago_cliente = pagos_cliente.annotate(
#         entrada=Case(
#             *[When(opcion_pago=opcion, then=F('monto')) for opcion, _ in OPCIONES_DE_PAGO],
#             default=0, output_field=DecimalField(max_digits=12, decimal_places=2)
#         )
#     ).values('opcion_pago').annotate(total_entrada=Sum('entrada'))

#     # Calcular la suma de las salidas por opciones de pago del proveedor
#     salidas_por_pago_proveedor = pagos_proveedor.annotate(
#         salida=Case(
#             *[When(opcion_pago=opcion, then=F('precio_proveedor')) for opcion, _ in OPCIONES_DE_PAGO],
#             default=0,
#             output_field=DecimalField(max_digits=12, decimal_places=2)
#         )
#     ).values('opcion_pago').annotate(total_salida=Sum('salida'))

#     # Combinar la información de entrada y salida por opción de pago
#     saldo_por_pago = []
#     for opcion, _ in OPCIONES_DE_PAGO:
#         entrada = next((item['total_entrada'] for item in entradas_por_pago_cliente if item['opcion_pago'] == opcion), 0)
#         salida = next((item['total_salida'] for item in salidas_por_pago_proveedor if item['opcion_pago'] == opcion), 0)
#         saldo = entrada - salida
#         saldo_por_pago.append((opcion.upper(), entrada, salida, saldo))

#     # Renderizar la plantilla con la información calculada y las fechas
#     return render(request, 'balance.html', {'saldo_por_pago': saldo_por_pago, 'start_date': start_date, 'end_date': end_date})

# @staff_member_required
# def pago_proveedor(request):
#     # Obtener la información requerida para la tabla
#     proveedores_info = Proveedor.objects.values('pais__nombre').annotate(
#         saldo=Sum('pagoproveedor__precio_proveedor', default=0,),
#         pendiente=Sum(
#             Case(
#                 When(pagoproveedor__estado='pendiente', then=F('pagoproveedor__precio_proveedor')),
#                 default=0,
#                 output_field=DecimalField(max_digits=12, decimal_places=2)
#             )
#         ),
#         pago_en_destino=Sum(
#             Case(
#                 When(pagoproveedor__opcion_pago='pago destino', then=F('pagoproveedor__precio_proveedor')),
#                 default=0,
#                 output_field=DecimalField(max_digits=12, decimal_places=2)
#             )
#         ),
#     )

#     return render(request, 'tabla_proveedores.html', {'proveedores_info': proveedores_info})


# @staff_member_required
# def calcular_ganancias(request):
#     proveedores = Proveedor.objects.all()
#     context = {'proveedores': proveedores}

#     form_incomplete = False  # Variable para controlar el mensaje de error

#     if request.method == 'POST':
#         proveedor_id = request.POST.get('proveedor')
#         precio_proveedor = request.POST.get('pago_proveedor')
#         pago_cliente = request.POST.get('pago_cliente')
#         comision_vendedor = request.POST.get('comision_vendedor')

#         if not (proveedor_id and precio_proveedor and pago_cliente and comision_vendedor):
#             form_incomplete = True
#         else:
#             # Convertir los valores a Decimal solo si no están vacíos
#             precio_proveedor = Decimal(precio_proveedor) if precio_proveedor else Decimal('0')
#             pago_cliente = Decimal(pago_cliente) if pago_cliente else Decimal('0')
#             comision_vendedor = Decimal(comision_vendedor) if comision_vendedor else Decimal('0')

#             proveedor = Proveedor.objects.get(pk=proveedor_id)
#             pago_proveedor = round(precio_proveedor - (precio_proveedor * (proveedor.comision / 100)), 2)
#             ganancia_bruto = pago_cliente - pago_proveedor
#             ganancia_usd_vendedor = round(pago_cliente * (comision_vendedor / 100), 2)
#             ganancia_gruv = ganancia_bruto - ganancia_usd_vendedor

#             ganancia_neta_porc = round((ganancia_gruv * 100) / ganancia_bruto, 2) if ganancia_bruto != 0 else 0

#             context.update({
#                 'comision_proveedor': proveedor.comision,
#                 'pago_proveedor': pago_proveedor,
#                 'ganancia_bruto': ganancia_bruto,
#                 'ganancia_usd_vendedor': ganancia_usd_vendedor,
#                 'ganancia_gruv': ganancia_gruv,
#                 'ganancia_neta_porc': ganancia_neta_porc,
#             })
            
#             # Si el formulario está incompleto o se hizo clic en "Nuevo", restablecer valores
#     if form_incomplete or 'limpiar_formulario' in request.POST:
#         context.update({
#             'pago_proveedor': None,
#             'pago_cliente': None,
#             'comision_vendedor': None,
#             'comision_proveedor': None,
#             'ganancia_bruto': None,
#             'ganancia_usd_vendedor': None,
#             'ganancia_gruv': None,
#             'ganancia_neta_porc': None,
#     })

#     context['form_incomplete'] = form_incomplete

#     return render(request, 'calcular_ganancias.html', context)

@staff_member_required
class VendedoresReporteView(TemplateView):
    template_name = 'reporte_vendedores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Realiza las consultas necesarias para obtener la información requerida
        vendedores = (
            Viaje.objects.select_related('vendedor')
            .annotate(volumen_ventas=Sum('pago_cliente_monto'))
            .annotate(ganancia_usd=Sum('ganancia_usd_vendedor'))
            .values('vendedor__nombre', 'volumen_ventas', 'ganancia_usd')
            .order_by('-volumen_ventas')
        )

        # Agrega el puesto a cada vendedor
        for i, vendedor in enumerate(vendedores, start=1):
            vendedor['puesto'] = i

        context['vendedores'] = vendedores
        return context