from django.contrib import admin
from django.urls import path, include

from catalogo.views import (home, 
                            index,
                            viaje_list,
                            TablasCombinadasView,
                            )


urlpatterns = [
    path('', home, name='home'),
    path('admin/', index, name='index'),
    path('', include('admin_datta.urls')),
    path('admin/', admin.site.urls),
    path('viaje-list/', viaje_list, name='viaje_list'),
    path('tablas-combinadas/', TablasCombinadasView.as_view(), name='tablas-combinadas'),
]
