
const refresh = document.getElementById("pfa-refresh");
const cambiosDomicilio = document.getElementById("pfa-cambio-domicilio");
const pedidosChacra = document.getElementById("pfa-pedido-chacra");
const asignacionMultiple = document.getElementById("pfa-multiple");

window.addEventListener("load", async () => {
    busca_pendientes();
    busca_asignados();
});


cambiosDomicilio.addEventListener('change', function () {
    busca_pendientes();
    busca_asignados();
});

pedidosChacra.addEventListener('change', function () {
    busca_pendientes();
    busca_asignados();
});

document.getElementById('pfa-refresh').addEventListener('click', function () {
    busca_pendientes();
    busca_asignados();
});

let dataTablePendientes, dataTableAsignados, dataTableRechazados;

$(document).ready(function () {
    // Inicializa DataTable para cada tabla individualmente
    $('#miTablaPendientes').DataTable({
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

    $('#miTablaAsignados').DataTable({
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

    $('#miTablaRechazados').DataTable({
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


const busca_pendientes = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("Tipo", getValueCheckBox());
        formData.append("Estado", 'P');

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-pendientes/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                            <tr class="pfa-tabla-fila">
                                <td class="pfa-tabla-celda"><input class="input-checkbox checkbox" type="checkbox" id="idCheck"
                                        name="idCheck" value="${datos.ID}"></td>
                                <td class="pfa-tabla-celda">${datos.ID}</td>
                                <td class="pfa-tabla-celda">${datos.Tipo}</td>
                                <td class="pfa-tabla-celda">${datos.Origen === '0' ? 'PLANTA': datos.Origen}</td>
                                <td class="pfa-tabla-celda">${datos.Solicita}</td>
                                <td class="pfa-tabla-celda">${datos.TipoDestino}</td>
                                <td class="pfa-tabla-celda">${datos.FechaPedido}</td>
                                <td class="pfa-tabla-celda">${datos.HoraPedido}</td>
                                <td class="pfa-tabla-celda">${datos.Zona === '0' ? '-' : datos.Zona}</td>
                                <td class="pfa-tabla-celda">${datos.Destino2 === '0' ? datos.Destino : datos.Destino2}</td>
                                <td class="pfa-tabla-celda">${datos.Especie}</td>
                                <td class="pfa-tabla-celda">${datos.Bins}</td>
                                <td class="pfa-tabla-celda">${datos.Vacios}</td>
                                <td class="pfa-tabla-celda">${datos.Cuellos}</td>
                                <td class="pfa-tabla-celda">
                                    <button class="boton-detalles" onclick="">
                                        <i class='bx material-symbols-outlined icon'>local_shipping</i>
                                    </button>
                                </td>
                                <td class="pfa-tabla-celda">
                                    <button class="boton-detalles" onclick="">
                                        <i class='bx material-symbols-outlined icon'>description</i>
                                    </button>
                                </td>
                            </tr>
                            `
            });
            if ($.fn.dataTable.isDataTable('#miTablaPendientes')) {
                $('#miTablaPendientes').DataTable().clear().destroy();
            }
            document.getElementById('pfa-tabla-pendientes').innerHTML = datos_he;
            dataTablePendientes = $('#miTablaPendientes').DataTable({
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

const busca_asignados = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("Tipo", getValueCheckBox());
        formData.append("Estado", 'A');

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-asignados/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                            <tr class="pfa-tabla-fila">
                                <td class="pfa-tabla-celda">${datos.ID}</td>
                                <td class="pfa-tabla-celda">${datos.Tipo}</td>
                                <td class="pfa-tabla-celda">${datos.Solicita}</td>
                                <td class="pfa-tabla-celda">${datos.TipoDestino}</td>
                                <td class="pfa-tabla-celda">${datos.FechaPedido}</td>
                                <td class="pfa-tabla-celda">${datos.Destino2 === '0' ? datos.Destino : datos.Destino2}</td>
                                <td class="pfa-tabla-celda">${datos.Chofer}</td>
                                <td class="pfa-tabla-celda">${datos.Transportista}</td>
                                <td class="pfa-tabla-celda">${datos.Camion}</td>
                                <td class="pfa-tabla-celda">
                                    <button class="boton-detalles" onclick="">
                                        <i class='bx material-symbols-outlined icon'>local_shipping</i>
                                    </button>
                                </td>
                                <td class="pfa-tabla-celda">
                                    <button class="boton-detalles" onclick="">
                                        <i class='bx material-symbols-outlined icon'>description</i>
                                    </button>
                                </td>
                            </tr>
                            `
            });
            if ($.fn.dataTable.isDataTable('#miTablaAsignados')) {
                $('#miTablaAsignados').DataTable().clear().destroy();
            }
            document.getElementById('pfa-tabla-asignados').innerHTML = datos_he;
            dataTableAsignados = $('#miTablaAsignados').DataTable({
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
                        "targets": [9, 10], 
                        "width": "3%",
                        "className": "dt-center"
                    }
                ]
            });
        } else {
            document.getElementById('pfa-tabla-asignados').innerHTML = ``;
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
















const modalOverlay = document.querySelector('.modal-overlay');
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

function getValueCheckBox() {
    if (cambiosDomicilio.checked && pedidosChacra.checked) {
        return '0';
    } else if (cambiosDomicilio.checked) {
        return 'U';
    } else if (pedidosChacra.checked) {
        return 'P';
    } else {
        return '0';
    }
}