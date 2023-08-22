"""
URL configuration for gruv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from catalogo.views import home, viaje_list, balance, pago_proveedor, calcular_ganancias


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('viaje-list/', viaje_list, name='viaje_list'),
    path('balance/', balance, name='balance'),
    path('proveedor-table/', pago_proveedor, name='tabla_proveedores'),
    path('calcular-ganancias/', calcular_ganancias, name='calcular_ganancias'),

]
