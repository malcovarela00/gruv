from django.contrib import admin
from django.urls import path, include, reverse_lazy

from django.views.generic.base import RedirectView

from catalogo.views import (home, 
                            index,
                            viaje_list,
                            TablasCombinadasView,
                            vendedores_reporte
                            )


urlpatterns = [
    path('', home, name='home'),
    path('admin/', index, name='index'),
    path('', include('admin_datta.urls')),
    path('admin/', admin.site.urls),
    path('viaje-list/', viaje_list, name='viaje_list'),
    path('tablas-combinadas/', TablasCombinadasView.as_view(), name='tablas-combinadas'),
    path('reporte-vendedores/', vendedores_reporte, name='reporte-vendedores'),
    
    path('accounts/profile/', RedirectView.as_view(url=reverse_lazy('admin:index'))),
]
