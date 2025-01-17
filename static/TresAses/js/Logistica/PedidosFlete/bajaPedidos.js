const desde = document.getElementById('fechaInicio');
const hasta = document.getElementById('fechaFinal');
const modalOverlay = document.querySelector('.modal-overlay');
let dataTablePendientes;


window.addEventListener("load", async () => {
    fechaActual();
    cargarOpcionesChoice(opcionesPedidos);
});

selector_pedidos.addEventListener('change', function () {
    busca_pedidos_flete();
});

document.getElementById('pfa-refresh').addEventListener('click', function () {
    busca_pedidos_flete();
});

document.getElementById('confirmBtn').addEventListener('click', function () {
    da_baja_pedido();
});

$(document).ready(function () {
    $('#miTablaPedidos').DataTable({
        "paging": false,
        "info": false,
        "ordering": true,
        "searching": true,
        "autoWidth": true,
        "language": {
            "search": "Buscar",
            "searchPlaceholder": "Escriba para buscar..."
        }
    });
});

const choicePedidos = new Choices('#selector_pedidos', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE TIPO PEDIDO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});


const busca_pedidos_flete = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Estado", getValueEstado());

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-pedidos/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda">${datos.ID}</td>
                        <td class="pfa-tabla-celda">${datos.Tipo}</td>
                        <td class="pfa-tabla-celda">${datos.Origen === '0' ? 'PLANTA' : datos.Origen}</td>
                        <td class="pfa-tabla-celda">${datos.Solicita}</td>
                        <td class="pfa-tabla-celda">${datos.TipoDestino}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.FechaPedido}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.HoraPedido}</td>
                        <td class="pfa-tabla-celda">${datos.Zona === '0' ? '-' : datos.Zona}</td>
                        <td class="pfa-tabla-celda">${datos.Destino2 === '0' ? datos.Destino : datos.Destino2}</td>
                        <td class="pfa-tabla-celda">${datos.Especie}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.Bins}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.Vacios}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.Cuellos}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">${datos.Estado}</td>
                        <td class="pfa-tabla-celda" style="text-align: center;">
                            <button class="boton-detalles ${datos.Estado === 'B' || datos.Estado === 'C' || datos.Estado === 'D' ? 'pf-boton-deshabilitado' : ''}" 
                                    onclick="openEliminar(${datos.ID});" 
                                    style="${datos.Estado === 'B' || datos.Estado === 'C' || datos.Estado === 'D' ? 'cursor: not-allowed; pointer-events: none;' : ''}">
                                <i class='bx material-symbols-outlined icon'>delete</i>
                            </button>
                        </td>
                    </tr>
                            `
            });
            if ($.fn.dataTable.isDataTable('#miTablaPedidos')) {
                $('#miTablaPedidos').DataTable().clear().destroy();
            }
            document.getElementById('pfa-tabla-pendientes').innerHTML = datos_he;
            dataTablePendientes = $('#miTablaPedidos').DataTable({
                "paging": false,
                "info": false,
                "ordering": true,
                "searching": true,
                "autoWidth": true,
                "language": {
                    "search": "Buscar: ",
                    "searchPlaceholder": "Escriba para buscar..."
                },
                "columnDefs": [
                    {
                        "targets": [10, 11, 12, 13, 14],
                        "width": "3%",
                        "className": "dt-center"
                    }
                ]
            });
        } else {
            document.getElementById('pfa-tabla-pendientes').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const da_baja_pedido = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        const IdPedidoFlete = document.getElementById('IdPedidoFlete').value;
        formData.append("IdPedidoFlete", IdPedidoFlete);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("baja-pedido/", options);
        const data = await response.json();
        closeProgressBar();
        closeEliminar();
        document.getElementById('content_pedido').innerHTML = `<input type="hidden" id="IdPedidoFlete" name="IdPedidoFlete" value="0"></input>`;
        if (data.Message == "Success") {
            busca_pedidos_flete();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota, color);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }

};

function getValueEstado() {
    return choicePedidos.getValue() ? choicePedidos.getValue().value : 'T';
}

function openEliminar(IdPedidoFlete) {
    document.getElementById('content_pedido').innerHTML = `<input type="hidden" id="IdPedidoFlete" name="IdPedidoFlete" value="${IdPedidoFlete}"></input>`;
    document.getElementById('confirmationPopup').style.display = 'flex';
}

function closeEliminar() {
    document.getElementById('content_pedido').innerHTML = `<input type="hidden" id="IdPedidoFlete" name="IdPedidoFlete" value="0"></input>`;
    document.getElementById('confirmationPopup').style.display = 'none';
}

function cargarOpcionesChoice(data) {
    const opciones = [];
    Object.keys(data).forEach((clave) => {
        opciones.push({
            value: clave,
            label: data[clave],
        });
    });
    choicePedidos.setChoices(opciones);
}

// Llamada a la función con el JSON
const opcionesPedidos = {
    "T": "TODO",
    "A": "ASIGNADOS",
    "B": "BAJA",
    "C": "CERRADOS",
    "D": "DESPACHADOS",
    "P": "PENDIENTES"
};





function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    const formattedDateDesde = `${ano}-${mes}-${'01'}`;
    desde.value = formattedDateDesde;
    hasta.value = formattedDate;
}

function openProgressBar() {
    modalOverlay.style.display = 'block';
}
function closeProgressBar() {
    modalOverlay.style.display = 'none';
}
document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popup").classList.remove("active");
});

function mostrarInfo(Message, Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}
