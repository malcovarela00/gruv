// Obtener los elementos del formulario
const pagoProveedor = document.getElementById('id_pago_proveedor_precio');
const comisionProveedor = document.getElementById('id_proveedor_comision');
const pagoCliente = document.getElementById('id_pago_cliente_monto');
const comisionVendedor = document.getElementById('id_comision_vendedor');
const gananciaBruto = document.getElementById('id_ganancia_bruto');
const gananciaUsdVendedor = document.getElementById('id_ganancia_usd_vendedor');
const gananciaGruv = document.getElementById('id_ganancia_gruv');
const gananciaNetaPorc = document.getElementById('id_ganancia_neta_porc');

// Función para calcular los valores de los campos
function calcularValores() {
    // Obtener los valores necesarios
    const precioProveedor = parseFloat(pagoProveedor.value);
    const comisionProveedorPorc = parseFloat(comisionProveedor.dataset.comision);
    const precioCliente = parseFloat(pagoCliente.value);
    const comisionVendedorPorc = parseFloat(comisionVendedor.value);

    // Calcular los valores necesarios
    const gananciaBrutoValor = precioCliente - precioProveedor;
    const gananciaUsdVendedorValor = (gananciaBrutoValor * comisionVendedorPorc) / 100;
    const gananciaGruvValor = gananciaBrutoValor - gananciaUsdVendedorValor;
    const gananciaNetaPorcValor = (gananciaGruvValor / precioCliente) * 100;
    const pagoProveedorValor = (precioCliente * comisionProveedorPorc) / 100;

  // Actualizar los valores de los campos
    gananciaBruto.value = gananciaBrutoValor.toFixed(2);
    gananciaUsdVendedor.value = gananciaUsdVendedorValor.toFixed(2);
    gananciaGruv.value = gananciaGruvValor.toFixed(2);
    gananciaNetaPorc.value = gananciaNetaPorcValor.toFixed(2);
    pagoProveedor.value = pagoProveedorValor.toFixed(2);
}

// Agregar un evento al formulario para calcular los valores al enviar el formulario
const form = document.getElementById('viaje_form');
form.addEventListener('submit', calcularValores);

// Calcular los valores al cargar la página
calcularValores();