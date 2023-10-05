from django.contrib import admin
from django.urls import path, include

from catalogo.views import (home, 
                            viaje_list,
                            TablasCombinadasView,
                            )


urlpatterns = [
    path('', home, name='home'),
    path('', include('admin_datta.urls')),
    path('admin/', admin.site.urls),
    path('viaje-list/', viaje_list, name='viaje_list'),
    #path('balance/', balance, name='balance'),
    path('tablas-combinadas/', TablasCombinadasView.as_view(), name='tablas-combinadas'),
]
