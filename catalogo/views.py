from django.shortcuts import render
from .models import Viaje, Saldo
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'home.html')

@staff_member_required
def viaje_list(request):
    viajes_with_saldo = Viaje.objects.select_related('saldo').all()
    return render(request, 'viaje_list.html', {'viajes': viajes_with_saldo})


