from django.contrib import admin
from django.urls import path, include

from catalogo.views import (TablasCombinadasView, 
                            home, 
                            viaje_list,
                            pago_proveedor,
                            balance,
                            VendedoresReporteView,
                            )
                            # calcular_ganancias,


urlpatterns = [
    path('', home, name='home'),
    path('', include('admin_datta.urls')),
    path('admin/', admin.site.urls),
    path('viaje-list/', viaje_list, name='viaje_list'),
    path('pago-proveedor/', pago_proveedor, name='pago-proveedores'),
    path('reporte-vendedores/', VendedoresReporteView.as_view(), name='reporte-vendedores'),
    path('balance/', balance, name='balance'),
    path('tablas-combinadas/', TablasCombinadasView.as_view(), name='tablas-combinadas'),
    # path('calcular-ganancias/', calcular_ganancias, name='calcular_ganancias'),
]
