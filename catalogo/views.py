from django.shortcuts import render
from .models import Viaje, Pais, Balance, Pago, OPCIONES_DE_PAGO
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View

from django.db.models import Sum, Case, When, F
from datetime import datetime
from django.utils import timezone


def home(request):
    return render(request, 'home.html')

def index(request):
    vendedores = vendedores_reporte(request)
    context = {
        'segment': 'index',
        'vendedores': vendedores,
        }
    return render(request, "templates_admin_data/pages/index.html", context)

@staff_member_required
def viaje_list(request):
    viajes = Viaje.objects.all()
    return render(request, 'viaje_list.html', {'viajes': viajes})


def obtener_balance(request):
    if request.method == 'GET':
        # Valores predeterminados para las fechas
        start_date = datetime.now().date()
        end_date = datetime.now().date()
        
        # Obtener las fechas del formulario si se proporcionan
        start_date_str = request.GET.get('start_date', start_date.strftime('%Y-%m-%d'))
        end_date_str = request.GET.get('end_date', end_date.strftime('%Y-%m-%d'))

        # Convertir las fechas a objetos datetime.date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Convertir las fechas a objetos datetime con zona horaria
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))

        saldo_por_pago = []
        for opcion in OPCIONES_DE_PAGO:
            # Obtén la suma de las entradas y salidas para esta opción de pago
            entradas = Balance.objects.filter(billetera=opcion[0], movimiento='entrada').aggregate(Sum('monto'))['monto__sum'] or 0
            salidas = Balance.objects.filter(billetera=opcion[0], movimiento='salida').aggregate(Sum('monto'))['monto__sum'] or 0
            # Calcula el saldo
            saldo = entradas - salidas
            # Agrega la opción de pago y su saldo a la lista
            saldo_por_pago.append((opcion[1], entradas, salidas, saldo))

    # Filtrar los pagos de clientes y proveedores por rango de fechas
    else:
        return 'no se puede hacer'

    # Renderiza la plantilla con los datos
    return saldo_por_pago, start_date, end_date


def pago_proveedor(request):
    proveedores_info = []

    paises = Pais.objects.values('nombre')

    for pais in paises:
        entradas = Viaje.objects.filter(proveedor__pais__nombre=pais['nombre']).exclude(
            pago_cliente_estado='cancelado').aggregate(entrada=Sum('pago_proveedor', default=0))

        salidas = Pago.objects.filter(pago_proveedor__nombre=pais['nombre']).aggregate(Sum('monto'))['monto__sum'] or 0

        saldo = (entradas['entrada'] or 0) - salidas

        proveedores_info.append({
            'pais': pais['nombre'],
            'saldo': saldo,
        })

    return proveedores_info


def vendedores_reporte(request):
    from django.db.models.functions import ExtractMonth

    mes_seleccionado = request.GET.get('mes')

    vendedores_query = Viaje.objects.annotate(
        mes=ExtractMonth('fecha_creacion')
    ).values('mes', 'vendedor__nombre').annotate(
        volumen_ventas=Sum('pago_cliente_monto'),
        ganancia_usd=Sum('ganancia_usd_vendedor')
    )

    if mes_seleccionado:
        vendedores_query = vendedores_query.filter(mes=mes_seleccionado)

    vendedores_query = vendedores_query.order_by('mes', '-volumen_ventas')

    vendedores = list(vendedores_query)
    for i, vendedor in enumerate(vendedores, start=1):
        vendedor['puesto'] = i

    meses = Viaje.objects.dates('fecha_creacion', 'month').values_list('fecha_creacion__month', flat=True).distinct()

    return render(request, 'nombre_de_tu_plantilla.html', {'vendedores': vendedores, 'meses': meses, 'mes_seleccionado': mes_seleccionado})

class TablasCombinadasView(View):
    def get(self, request):
        proveedores_info = pago_proveedor(request)
        vendedores = vendedores_reporte(request)
        saldo_por_pago, start_date, end_date = obtener_balance(request)

        return render(request, 'tablas_combinadas.html', {
            'proveedores_info': proveedores_info, 
            'vendedores': vendedores,
            'saldo_por_pago': saldo_por_pago,
            'start_date': start_date,
            'end_date': end_date
            })