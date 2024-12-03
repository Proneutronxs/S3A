let map;
const refresh = document.getElementById("pfa-refresh");
const cambiosDomicilio = document.getElementById("pfa-cambio-domicilio");
const pedidosChacra = document.getElementById("pfa-pedido-chacra");
const asignacionMultiple = document.getElementById("pfa-multiple");
const popup = document.getElementById('pop_up_detalles');


window.addEventListener("load", async () => {
    busca_pendientes();
    busca_asignados();
    listar_choferes();
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

document.getElementById('pfa-refresh-choferes').addEventListener('click', function () {
    listar_choferes();
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
                                <td class="pfa-tabla-celda">${datos.Origen === '0' ? 'PLANTA' : datos.Origen}</td>
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

const listar_choferes = async () => {
    openProgressBar();
    try {
        const response = await fetch("listar-choferes/");
        const data = await response.json();
        closeProgressBar();
        if (data.Message === "Success") {
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                            <div class="pfs-card">
                                <div class="pfs-card-header">
                                    <div class="pfs-card-icon">
                                        <i class="material-symbols-outlined">person</i>
                                    </div>
                                    <div class="pfs-card-info">
                                        <h3 class="pfs-card-title">${datos.Chofer}</h3>
                                        <p class="pfs-card-details">${datos.Transporte} - ${datos.Camion}</p>
                                    </div>
                                </div>
                                <div class="pfs-card-actions">
                                    <button class="pfs-card-button" onclick="detalle_destinos(${datos.IdCA});">
                                        <i class="material-symbols-outlined pfa-btn-submit">description</i>
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
        closeProgressBar();
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