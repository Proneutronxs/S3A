let map;
let IdTransporte;
let IdCamion;
let IdAcoplado;
let dataCamiones = [];
let dataAcoplados = [];
const refresh = document.getElementById("pfa-refresh");
const cambiosDomicilio = document.getElementById("pfa-cambio-domicilio");
const pedidosChacra = document.getElementById("pfa-pedido-chacra");
const asignacionMultiple = document.getElementById("pfa-multiple");
const popup = document.getElementById('pop_up_detalles');
const cancelAsig = document.getElementById('btn-cancel-asig');
const openAsig = document.getElementById('popup-container-pfa-asig');
const modalOverlay = document.querySelector('.modal-overlay');
const inputVacios = document.getElementById('input-cantidad-vacios');
const tituloAsignacion = document.getElementById('titulo-asignaciones');

let dataTablePendientes, dataTableAsignados, dataTableRechazados;

window.addEventListener("load", async () => {
    busca_pendientes();
    busca_asignados();
    listar_choferes();
    busca_rechazados();
});

cambiosDomicilio.addEventListener('change', function () {
    busca_pendientes();
    busca_asignados();
    busca_rechazados();
});

pedidosChacra.addEventListener('change', function () {
    busca_pendientes();
    busca_asignados();
    busca_rechazados();
});

document.getElementById('pfa-refresh').addEventListener('click', function () {
    busca_pendientes();
    busca_asignados();
    busca_rechazados();
});

document.getElementById('pfa-refresh-choferes').addEventListener('click', function () {
    listar_choferes();
});

document.getElementById('pfa-multiple').addEventListener('click', function () {
    multiple_viaje();
});

document.getElementById('confirmBtn').addEventListener('click', function () {
    mover_rechazados_pendientes();
});

document.getElementById('cancelBtn').addEventListener('click', function () {
    ocultarPopupMover();
});

document.getElementById('btn-acept-asig').addEventListener('click', function () {
    const valorAsignacion = document.getElementById('valueAsignacion').value;
    if (valorAsignacion === 'MV') {
        if (condicionales_asignaciones()) {
            guardar_asignacion_multiple();
        }
    } else if (valorAsignacion === 'SV') {
        if (condicionales_asignaciones()) {
            guardar_asignacion_individual();
        }
    }
});

selector_choferes.addEventListener("change", (event) => {
    const parsedCustomProperties = JSON.parse(event.currentTarget.selectedOptions[0].dataset.customProperties);
    IdTransporte = parsedCustomProperties.IdTransporte;
    choiceTransportes.setChoiceByValue(IdTransporte);
    choiceTransportes.disable();
    choiceCamiones.clearChoices();
    choiceCamiones.removeActiveItems();
    choiceAcoplados.clearChoices();
    choiceAcoplados.removeActiveItems();
    cargarCamiones(IdTransporte);
    IdCamion = parsedCustomProperties.IdCamion;
    choiceCamiones.setChoiceByValue(IdCamion);
    cargarAcoplados(IdTransporte);
    IdAcoplado = parsedCustomProperties.IdAcoplado;
    choiceAcoplados.setChoiceByValue(IdAcoplado);
});

selector_camiones.addEventListener("change", (event) => {
    choiceTransportes.setChoiceByValue(IdTransporte);
    cargarCamiones(IdTransporte);
});

const choiceVacios = new Choices('#selector_vacios', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE UBICACIÓN VACÍOS',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceChoferes = new Choices('#selector_choferes', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CHOFER',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceTransportes = new Choices('#selector_transportes', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE TRANSPORTE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceCamiones = new Choices('#selector_camiones', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CAMIÓN',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceAcoplados = new Choices('#selector_acoplados', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ACOPLADO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

$(document).ready(function () {
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
                                <td class="pfa-tabla-celda" style="text-align: center;">
                                    <button class="boton-detalles" onclick="simple_viaje(${datos.ID})">
                                        <i class='bx material-symbols-outlined icon'>local_shipping</i>
                                    </button>
                                </td>
                                <td class="pfa-tabla-celda" style="text-align: center;">
                                    <button class="boton-detalles" onclick="detalles_pedidos(${datos.ID});">
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
                                <td class="pfa-tabla-celda" style="text-align: center;">${datos.ID}</td>
                                <td class="pfa-tabla-celda">${datos.Tipo}</td>
                                <td class="pfa-tabla-celda">${datos.Solicita}</td>
                                <td class="pfa-tabla-celda">${datos.TipoDestino}</td>
                                <td class="pfa-tabla-celda" style="text-align: center;">${datos.FechaPedido}</td>
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
                                    <button class="boton-detalles" onclick="detalles_pedidos(${datos.ID});">
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

const busca_rechazados = async () => {
    try {
        const response = await fetch("listar-rechazados/");
        const data = await response.json();
        if (data.Message === "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                <tr class="pfa-tabla-fila">
                    <td class="pfa-tabla-celda" style="text-align: center;">${datos.ID_CVN}</td>
                    <td class="pfa-tabla-celda" style="text-align: center;">${datos.Chofer}</td>
                    <td class="pfa-tabla-celda" style="text-align: center;">${datos.Fecha}</td>
                    <td class="pfa-tabla-celda" style="text-align: center;">${datos.Cantidad}</td>
                    <td class="pfa-tabla-celda" style="text-align: center;">
                        <button class="boton-detalles" onclick="detalles_rechazados(${datos.ID_CVN});">
                            <i class='bx material-symbols-outlined icon'>description</i>
                        </button>
                    </td>
                    <td class="pfa-tabla-celda" style="text-align: center;">
                        <button class="boton-detalles" onclick="mostrarPopupMover(${datos.ID_CVN});">
                            <i class='bx material-symbols-outlined icon'>arrow_upward</i>
                        </button>
                    </td>
                </tr>
                `
            });

            if ($.fn.dataTable.isDataTable('#miTablaRechazados')) {
                $('#miTablaRechazados').DataTable().clear().destroy();
            }
            document.getElementById('listado_rechazados').innerHTML = datos_he;
            dataTableAsignados = $('#miTablaRechazados').DataTable({
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
                        "targets": [4, 5],
                        "width": "10%",
                        "className": "dt-center"
                    }
                ]
            });
        } else {
            document.getElementById('listado_rechazados').innerHTML = ``;
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const listar_choferes = async () => {
    try {
        const response = await fetch("listar-choferes/");
        const data = await response.json();
        if (data.Message === "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                            <div class="pfs-card">
                                <div class="pfs-card-header">
                                    <div class="pfs-card-info">
                                        <h3 class="pfs-card-title">${datos.Chofer}</h3>
                                        <p class="pfs-card-details">${datos.Transporte} - ${datos.Camion}</p>
                                    </div>
                                </div>
                                <div class="pfs-card-actions">
                                    <button class="pfs-card-button" onclick="detalle_destinos(${datos.IdCA});">
                                        <i class="material-symbols-outlined pfa-btn-submit">description</i>
                                    </button>
                                    <button class="pfs-card-button" onclick="">
                                        <i class="material-symbols-outlined pfa-btn-submit">contrast_square</i>
                                    </button>
                                    <button class="pfs-card-button" onclick="mapeo_ultima_ubicacion(${datos.IdCA});">
                                        <i class="material-symbols-outlined pfa-btn-submit">location_on</i>
                                    </button>
                                </div>
                            </div>
                            `
            });
            document.getElementById('pfa-contenedor-choferes').innerHTML = datos_he;
        } else {
            document.getElementById('pfa-contenedor-choferes').innerHTML = ``;
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const mapeo_ultima_ubicacion = async (ID_CA) => {
    openProgressBar();
    try {

        const formData = new FormData();
        formData.append("Chofer", ID_CA);

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch("mapeo-ultima-ubicacion/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            abrirUltimaUbicacion();
            const lat = parseFloat(data.Datos.Latitud);
            const lng = parseFloat(data.Datos.Longitud);
            const mapContainer = document.getElementById('pfa_mapeo_actual');
            if (map) {
                map.off();
                map.remove();
            }
            map = L.map(mapContainer).setView([lat, lng], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
            L.marker([lat, lng]).addTo(map)
                .bindPopup(`<strong>${data.Datos.Chofer}</strong><br>${data.Datos.Hace}`)
                .openPopup();
        } else {
            var nota = data.Nota;
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

const detalles_pedidos = async (IdPedidoFlete) => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("IdPedidoFlete", IdPedidoFlete);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("mostrar-detalles/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                        <div class="popup-columns">
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>ID PEDIDO:</strong> ${datos.ID}
                                </div>
                                <div class="info-item">
                                    <strong>SOLICITA:</strong> ${datos.Solicita}
                                </div>
                                <div class="info-item">
                                    <strong>ORIGEN:</strong> ${datos.Origen}
                                </div>
                                <div class="info-item">
                                    <strong>DESTINO:</strong> ${datos.Destino}
                                </div>
                                <div class="info-item">
                                    <strong>FECHA:</strong> ${datos.FechaPedido}
                                </div>
                                <div class="info-item">
                                    <strong>HORA:</strong> ${datos.HoraPedido}
                                </div>
                                <div class="info-item">
                                    <strong>HORA REQUERIDO:</strong> ${datos.HoraRequerido}
                                </div>
                                <div class="info-item">
                                    <strong>TRANSPORTE:</strong> ${datos.Transportista}
                                </div>
                                <div class="info-item">
                                    <strong>CHOFER:</strong> ${datos.Chofer}
                                </div>
                            </div>
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>TIPO:</strong> ${datos.Tipo}
                                </div>
                                <div class="info-item">
                                    <strong>CARGA:</strong> ${datos.TipoDestino}
                                </div>
                                <div class="info-item">
                                    <strong>ESPECIE:</strong> ${datos.Especie}
                                </div>
                                <div class="info-item">
                                    <strong>VARIEDAD:</strong> ${datos.Variedad}
                                </div>
                                <div class="info-item">
                                    <strong>BINS:</strong> ${datos.Bins}
                                </div>
                                <div class="info-item">
                                    <strong>VACÍOS:</strong> ${datos.Vacios}
                                </div>
                                <div class="info-item">
                                    <strong>CUELLO:</strong> ${datos.Cuellos}
                                </div>
                                <div class="info-item">
                                    <strong>CAMION:</strong> ${datos.Camion}
                                </div>
                                <div class="info-item">
                                    <strong>ACOPLADO:</strong> ${datos.Acoplado}
                                </div>
                            </div>
                        </div>
                        <div class="popup-observaciones">
                            <h3>Observaciones</h3>
                            <textarea rows="4" placeholder="Sin Observaciones ..." disabled>
                                    ${datos.Obs}
                            </textarea>
                        </div>
                        `
            });
            document.getElementById('pfa-titulo-popup').innerHTML = `<h2>DETALLE PEDIDO FLETE</h2>`;
            document.getElementById('content-detalles-pedidos').innerHTML = datos_he;
            masDetalles();
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

const detalles_rechazados = async (ID_CVN) => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("ID_CVN", ID_CVN);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("mostrar-detalles-rechazados/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            document.getElementById('pfa-titulo-popup').innerHTML = `<h2 style="color: red;">DETALLE VIAJE RECHAZADO</h2>`;

            const datos = data.Datos;
            document.getElementById('content-detalles-pedidos').innerHTML = `
                        <div class="popup-columns">
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>ID VIAJE:</strong> ${datos.ID_CVN}
                                </div>
                                <div class="info-item">
                                    <strong>CHOFER:</strong> ${datos.Chofer}
                                </div>
                            </div>
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>FECHA:</strong> ${datos.Fecha}
                                </div>
                                <div class="info-item">
                                    <strong></strong> 
                                </div>
                            </div>
                        </div>
                        `;

            let tabla = `
                        <table class="pfa-detalle-destinos-tabla">
                            <thead>
                                <tr>
                                    <th>ID PEDIDO</th>
                                    <th>ORIGEN</th>
                                    <th>DESTINO</th>
                                    <th>SOLICITA</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            data.Tabla.forEach((fila) => {
                tabla += `
                            <tr>
                                <td>${fila.IdPedidoFlete}</td>
                                <td>${fila.Origen}</td>
                                <td>${fila.Destino}</td>
                                <td>${fila.Solicita}</td>
                            </tr>
              `;
            });

            tabla += `
                            </tbody>
                        </table>
            `;

            document.getElementById('content-detalles-pedidos').innerHTML += tabla;
            masDetalles();
        }
        else {
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

const detalle_destinos = async (ID_CA) => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("ID_CA", ID_CA);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("viaje-detalles/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            let datos_he = `
              <div style="text-align: center;">
                <Strong>RETIRA VACÍOS EN ${data.LugarVacios}: </Strong> ${data.HoraVacios}
              </div>
              <table class="pfa-detalle-destinos-tabla">
                <thead>
                  <tr>
                    <th>ID PEDIDO</th>
                    <th>ORIGEN</th>
                    <th>DESTINO</th>
                    <th>HORA LLEGADA</th>
                  </tr>
                </thead>
                <tbody>
            `;

            data.Datos.forEach((datos) => {
                datos_he += `
                <tr>
                  <td>${datos.IdPF}</td>
                  <td>${datos.Origen}</td>
                  <td>${datos.Destino}</td>
                  <td>${datos.HoraLlegada}</td>
                </tr>
              `;
            });

            datos_he += `
                </tbody>
              </table>
            `;

            document.getElementById('pfa-titulo-popup').innerHTML = `<h2>DETALLES DEL VIAJE</h2>`;
            document.getElementById('content-detalles-pedidos').innerHTML = datos_he;
            masDetalles();
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

const multiple_viaje = async () => {
    if (verificarCheckbox()) {
        openProgressBar();
        try {
            const checkboxes = document.querySelectorAll('.input-checkbox:checked');
            const formData = new FormData();

            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    formData.append('IdPedidoFlete', checkbox.value);
                }
            });

            const options = {
                method: 'POST',
                headers: {
                },
                body: formData
            };

            const response = await fetch("verificacion-carga-combox/", options);
            const data = await response.json();
            closeProgressBar();
            if (data.Message == "Success") {
                limpiar_choices_input();
                let datos_he = ``;
                data.Destinos.forEach((datos) => {
                    datos_he += `   
                    <tr>
                        <td>${datos.IdPF}</td>
                        <td>${datos.Destino}</td>
                    </tr>
                    `
                });
                document.getElementById('pfa-asig-destinos-tabla').innerHTML = datos_he;

                let result = [];
                result.push();
                data.Choferes.forEach((datos) => {
                    result.push({
                        value: datos.IdChofer,
                        label: datos.Chofer,
                        customProperties: JSON.stringify({ IdTransporte: datos.IdTransporte, IdCamion: datos.IdCamion, IdAcoplado: datos.IdAcoplado })
                    });
                });
                choiceChoferes.setChoices(result, 'value', 'label', true);

                let result1 = [];
                result1.push();
                data.Vacios.forEach((datos) => {
                    result1.push({ value: datos.IdVacios, label: datos.Nombre });
                });
                choiceVacios.setChoices(result1, 'value', 'label', true);

                let result2 = [];
                result2.push();
                data.Transportes.forEach((datos) => {
                    result2.push({ value: datos.IdTransporte, label: datos.Transporte });
                });
                choiceTransportes.setChoices(result2, 'value', 'label', true);

                dataCamiones.splice(0, dataCamiones.length);
                dataAcoplados.splice(0, dataAcoplados.length);
                dataCamiones = data.Camiones;
                dataAcoplados = data.Acoplados;
                tituloAsignacion.innerHTML = `
                    ASIGNACION MULTIPLE
                    <input type="hidden" id="valueAsignacion" name="miInputOculto" value="MV">                
                `;
                asignar();
            } else {
                document.getElementById('pfa-asig-destinos-tabla').innerHTML = ``;
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

    } else {
        mostrarInfo("Debe seleccionar al menos 2 Pedidos de Flete y menos de 5.", "red")
    }

};

const simple_viaje = async (IdPedidoFlete) => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append('IdPedidoFlete', IdPedidoFlete);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("verificacion-carga-combox/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            limpiar_choices_input();
            let datos_he = ``;
            data.Destinos.forEach((datos) => {
                datos_he += `   
                    <tr>
                        <td>${datos.IdPF}</td>
                        <td>${datos.Destino}</td>
                    </tr>
                    <input type="hidden" id="simpleID" name="miInputOculto" value="${datos.IdPF}">
                    `
            });
            document.getElementById('pfa-asig-destinos-tabla').innerHTML = datos_he;

            let result = [];
            result.push();
            data.Choferes.forEach((datos) => {
                result.push({
                    value: datos.IdChofer,
                    label: datos.Chofer,
                    customProperties: JSON.stringify({ IdTransporte: datos.IdTransporte, IdCamion: datos.IdCamion, IdAcoplado: datos.IdAcoplado })
                });
            });
            choiceChoferes.setChoices(result, 'value', 'label', true);

            let result1 = [];
            result1.push();
            data.Vacios.forEach((datos) => {
                result1.push({ value: datos.IdVacios, label: datos.Nombre });
            });
            choiceVacios.setChoices(result1, 'value', 'label', true);

            let result2 = [];
            result2.push();
            data.Transportes.forEach((datos) => {
                result2.push({ value: datos.IdTransporte, label: datos.Transporte });
            });
            choiceTransportes.setChoices(result2, 'value', 'label', true);

            dataCamiones.splice(0, dataCamiones.length);
            dataAcoplados.splice(0, dataAcoplados.length);
            dataCamiones = data.Camiones;
            dataAcoplados = data.Acoplados;
            tituloAsignacion.innerHTML = `
            ASIGNACION SIMPLE
            <input type="hidden" id="valueAsignacion" name="miInputOculto" value="SV">                
            `;
            asignar();
        } else {
            document.getElementById('pfa-asig-destinos-tabla').innerHTML = ``;
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

const guardar_asignacion_multiple = async () => {
    openProgressBar();
    try {
        const checkboxes = document.querySelectorAll('.input-checkbox:checked');
        const formData = new FormData();
        formData.append("IdChofer", choiceChoferes.getValue().value);
        formData.append("NombreChofer", choiceChoferes.getValue().label);
        formData.append("IdTransporte", choiceTransportes.getValue().value);
        formData.append("IdCamion", choiceCamiones.getValue().value);
        formData.append("IdAcoplado", getValueAcoplados());
        formData.append("CantVacios", getValueCantidadVacios());
        formData.append("IdUbiVacios", getValueVacios());

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('IdPedidosFletes', checkbox.value);
            }
        });

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("asignaciones-multiples/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            busca_pendientes();
            busca_asignados();
            openAsig.style.display = 'none';
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

const guardar_asignacion_individual = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        const simpleID = document.getElementById('simpleID').value;
        formData.append("IdChofer", choiceChoferes.getValue().value);
        formData.append("NombreChofer", choiceChoferes.getValue().label);
        formData.append("IdTransporte", choiceTransportes.getValue().value);
        formData.append("IdCamion", choiceCamiones.getValue().value);
        formData.append("IdAcoplado", getValueAcoplados());
        formData.append("CantVacios", getValueCantidadVacios());
        formData.append("IdUbiVacios", getValueVacios());
        formData.append("IdPedidoFlete", simpleID);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("asignaciones-individuales/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            busca_pendientes();
            busca_asignados();
            openAsig.style.display = 'none';
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

const mover_rechazados_pendientes = async () => {
    openProgressBar();
    try {
        const id_cvn = document.getElementById('id_cvn_mover');
        const formData = new FormData();
        formData.append("ID_CVN", id_cvn.value);

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch("liberar-rechazados/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            busca_rechazados();
            busca_pendientes();
            ocultarPopupMover();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
        } else {
            var nota = data.Nota;
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

function condicionales_asignaciones() {
    if (!choiceAcoplados.getValue()) {
        var nota = 'Debe seleccionar el chofer.';
        var color = "red";
        mostrarInfo(nota, color);
        return false;
    }
    return true;
}

function getValueAcoplados() {
    return choiceAcoplados.getValue() ? choiceAcoplados.getValue().value : '';
}

function getValueVacios() {
    return choiceVacios.getValue() ? choiceVacios.getValue().value : '';
}

function getValueCantidadVacios() {
    const valor = inputVacios.value;
    if (isNaN(valor) || valor === '') {
        return '';
    } else {
        return valor;
    }
}

function validarCantidad() {
    const valor = inputVacios.value;
    if (valor < 1 || valor > 65) {
        inputVacios.style.border = '4px solid red';
    } else {
        inputVacios.style.border = '';
    }
}

inputVacios.addEventListener('input', validarCantidad);

function limpiar_choices_input() {
    choiceVacios.clearChoices();
    choiceVacios.removeActiveItems();
    choiceChoferes.clearChoices();
    choiceChoferes.removeActiveItems();
    choiceTransportes.clearChoices();
    choiceTransportes.removeActiveItems();
    choiceCamiones.clearChoices();
    choiceCamiones.removeActiveItems();
    choiceAcoplados.clearChoices();
    choiceAcoplados.removeActiveItems();
    inputVacios.value = '';
}

function cargarCamiones(idTransporte) {
    choiceCamiones.clearChoices();
    choiceCamiones.removeActiveItems();
    const camiones = dataCamiones.find((camion) => camion.IdTransporte === idTransporte);
    if (camiones) {
        const opciones = camiones.Items.map((item) => ({
            value: item.IdCamion,
            label: item.Descripcion,
        }));
        choiceCamiones.setChoices(opciones);
    }
}

function cargarAcoplados(idTransporte) {
    choiceAcoplados.clearChoices();
    choiceAcoplados.removeActiveItems();
    const acoplados = dataAcoplados.find((camion) => camion.IdTransporte === idTransporte);
    if (acoplados) {
        const opciones = acoplados.Items.map((item) => ({
            value: item.IdAcoplado,
            label: item.Descripcion,
        }));
        choiceAcoplados.setChoices(opciones);
    }
}

function verificarCheckbox() {
    const checkboxes = document.querySelectorAll('#miTablaPendientes input[type="checkbox"]');
    const seleccionados = Array.prototype.filter.call(checkboxes, (checkbox) => checkbox.checked);

    if (seleccionados.length > 1 && seleccionados.length < 5) {
        return true;
    } else {
        return false;
    }
}

function asignar() {
    openAsig.style.display = 'flex'
}

cancelAsig.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.input-checkbox:checked');

    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    openAsig.style.display = 'none';
});

function abrirUltimaUbicacion() {
    document.getElementById('pfa-lu-popup').style.display = 'flex';
}

document.getElementById('pfa-lu-popup-cerrar').addEventListener('click', function () {
    document.getElementById('pfa-lu-popup').style.display = 'none';
});

function masDetalles() {
    popup.style.display = 'flex';
}

closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none';
});

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

function mostrarPopupMover(ID_CVN) {
    document.getElementById('number_cvn').innerHTML = `
        <input type="hidden" id="id_cvn_mover" name="dataOculta" value="${ID_CVN}">
    `;
    document.getElementById('confirmationPopup').style.display = 'flex';
}

function ocultarPopupMover() {
    document.getElementById('confirmationPopup').style.display = 'none';
}

function getValueCheckBox() {
    if (cambiosDomicilio.checked && pedidosChacra.checked) {
        return '0';
    } else if (cambiosDomicilio.checked) {
        return 'U';
    } else if (pedidosChacra.checked) {
        return 'P';
    } else {
        return 'T';
    }
}