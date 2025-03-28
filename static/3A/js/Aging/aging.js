const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
let jsonDatos;


window.addEventListener("load", async () => {
    dataInicial();
    fechaActual();
});

selector_cliente.addEventListener("change", (event) => {
    changeClean();
    dataSubItems();
});

selector_sub_cliente.addEventListener("change", (event) => {
    changeClean();
});

desde.addEventListener("change", (event) => {
    changeClean();
});

hasta.addEventListener("change", (event) => {
    changeClean();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    if (!choiceCliente.getValue()) {
        mostrarInfo("Por favor, seleccione un Cliente.", "red");
    } else {
        dataDateTable();
    }
});

document.getElementById('ver-dinamico-button').addEventListener('click', function () {
    openLoading();
    innerPopAll();
    dataDateTableDynamic();
});

const choiceCliente = new Choices('#selector_cliente', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE MAIN CLIENTE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceSubCliente = new Choices('#selector_sub_cliente', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CLIENTE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

$(document).ready(function () {
    $('#tableDataCuentas').DataTable({
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

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("clientes-principales/");
        const data = await response.json();
        closeLoading();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.IdCuenta, label: datos.Descripcion,
                    customProperties: JSON.stringify({ Principal: datos.Principal })
                });
            });
            choiceCliente.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const dataSubItems = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdCliente", getValuePSubCliente());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("sub-clientes/", options);
        const data = await response.json();
        closeLoading();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.IdCuenta, label: datos.Descripcion });
            });
            choiceSubCliente.clearChoices();
            choiceSubCliente.removeActiveItems();
            choiceSubCliente.setChoices(result, 'value', 'label', true);
        } else {
            choiceSubCliente.clearChoices();
            choiceSubCliente.removeActiveItems();
        }
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const dataDateTable = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCliente", getValueCliente());
        formData.append("IdSubCliente", getValueSubCliente());
        formData.append("Tipo", "TT");
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("cuentas-clientes/", options);
        const data = await response.json();
        closeLoading();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            jsonDatos = null;
            jsonDatos = data.Datos;
            let datosTabla = ``;
            data.Datos.forEach((datos) => {
                datosTabla += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda text-center">${datos.Season}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Week}</td>
                        <td class="pfa-tabla-celda text-right">${formatMoneda(datos.Amount)}</td>
                        <td class="pfa-tabla-celda text-left">${datos.MainClient}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Client}</td>
                        <td class="pfa-tabla-celda text-center">${datos.FwInvoice}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Order}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Trader}</td>
                        <td class="pfa-tabla-celda text-center">${formatFecha(datos.DepartureDate)}</td>
                        <td class="pfa-tabla-celda text-center">${datos.TT}</td>
                        <td class="pfa-tabla-celda text-center">${formatFecha(datos.ArrivalDate)}</td>
                        <td class="pfa-tabla-celda text-center">${formatFecha(datos.EstimPaymDate)}</td>
                        <td class="pfa-tabla-celda text-center">${datos.EstimPaymWeek}</td>
                        <td class="pfa-tabla-celda text-right">${formatMoneda(datos.TotalPaid)}</td>
                        <td class="pfa-tabla-celda text-center">${formatFecha(datos.PaymDate)}</td>
                        <td class="pfa-tabla-celda text-center">${datos.PaymWeek}</td>
                        <td class="pfa-tabla-celda text-right">${formatMoneda(datos.Balance)}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Status}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Country}</td>
                    </tr>
                `
            });

            if ($.fn.dataTable.isDataTable('#tableDataCuentas')) {
                $('#tableDataCuentas').DataTable().clear().destroy();
            }
            document.getElementById('pfa-tabla-DataCuentas').innerHTML = datosTabla;
            dataTableAsignados = $('#tableDataCuentas').DataTable({
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
                        "targets": [0, 1],
                        "width": "1%",
                        "className": "dt-center"
                    },
                    {
                        "targets": [3, 4],
                        "width": "13%",
                    },
                    {
                        "targets": [5, 8, 10, 11, 12, 14, 15],
                        "width": "4%",
                    }
                ]
            });
            document.getElementById("class-bt-dinamico").style.display = "block";
            document.getElementById("class-bt-download").style.display = "block";
        } else {
            document.getElementById('pfa-tabla-DataCuentas').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const dataDateTableDynamic = async () => {
    try {
        jsonDatos.forEach(item => {
            item.Balance = parseFloat(item.Balance);
        });

        $("#pivot-table").pivotUI(jsonDatos, {
            rows: ["Country", "Client", "FwInvoice", "Order", "Trader", "DepartureDate"],
            cols: ["EstimPaymWeek"],
            aggregatorName: "Sum",
            vals: ["Balance"],
            rendererName: "Table",
            hiddenAttributes: [
                "rows", "cols", "vals", "aggregatorName", "rendererName"
            ],
            hiddenFromDragDrop: true,
            menuLimit: 0,
            autoSortUnusedAttrs: false,
            filter: function (record) {
                return record.Status === "PENDIENTE";
            }
        });
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const descargarArchivo = async (tipo, name) => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCliente", getValueCliente());
        formData.append("IdSubCliente", getValueSubCliente());
        formData.append("Tipo", tipo);

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch('cuentas-clientes/', options);
        const contentType = response.headers.get('content-type');
        closeLoading();
        if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            const blob = await response.blob();
            const excelURL = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = excelURL;
            a.style.display = 'none';
            a.download = name + obtenerFechaHoraActual() + '.xlsx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(excelURL);
        } else {
            const data = await response.json();
            if (data.Message == "Not Authenticated") {
                window.location.href = data.Redirect;
            } else {
                var nota = data.Nota;
                var color = "red";
                mostrarInfo(nota, color);
            }
        }
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

function formatMoneda(texto) {
    const num = parseFloat(texto.replace(/[^0-9.-]/g, ''));
    if (isNaN(num)) {
        return '';
    }
    return `U$S ${num.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatFecha(fecha) {
    const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    if (fecha === '01/01/1900') {
        return '-';
    }
    const [dia, mes, año] = fecha.split('/');
    const fechaObj = new Date(`${mes}/${dia}/${año}`);
    if (isNaN(fechaObj)) {
        return '-';
    }
    const diaFecha = fechaObj.getDate();
    const mesFecha = meses[fechaObj.getMonth()];
    return `${diaFecha} - ${mesFecha}`;
}

function obtenerFechaHoraActual() {
    const fecha = new Date();
    const anio = fecha.getFullYear();
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
    const dia = fecha.getDate().toString().padStart(2, '0');
    const hora = fecha.getHours().toString().padStart(2, '0');
    const minutos = fecha.getMinutes().toString().padStart(2, '0');
    const segundos = fecha.getSeconds().toString().padStart(2, '0');

    return `${anio}_${mes}_${dia}_${hora}_${minutos}_${segundos}`;
}

function getValueCliente() {
    return choiceCliente.getValue() ? choiceCliente.getValue().value : '';
}

function getValuePSubCliente() {
    const selectedValue = choiceCliente.getValue();
    if (selectedValue) {
        const customProperties = JSON.parse(selectedValue.customProperties);
        return customProperties.Principal;
    }
    return '';
}

function getValueSubCliente() {
    return choiceSubCliente.getValue() ? choiceSubCliente.getValue().value : '';
}

function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    const formattedDateDesde = `${ano}-${'01'}-${'01'}`;
    desde.value = formattedDateDesde;
    hasta.value = formattedDate;
}

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

function openLoading() {
    loadingContainer.style.display = 'flex';
}

function closeLoading() {
    loadingContainer.style.display = 'none';
}

document.querySelector('.pop-all-close-btn').addEventListener('click', function () {
    document.querySelector('.pop-all-overlay').style.display = 'none';
});

function innerPopAll() {
    const all_content = document.getElementById("dynamic");
    all_content.innerHTML = `
        <div class="dynamic-table-pivot">
            <div id="pivot-table"></div>
        </div>
        <div style="text-align: right; margin-top: 10px;">
            <div class="vr-col-icon" id="class-bt-download-pv">
            <a onclick="descargarArchivo('TD','Proyeccion_x_semana_')">
                <i class='bx material-symbols-outlined icon'>download</i>
            </a>
            </div>
        </div>
    `;
    document.querySelector('.pop-all-overlay').style.display = 'flex';
}

function changeClean() {
    jsonDatos = null;
    document.getElementById('pfa-tabla-DataCuentas').innerHTML = ``;
    document.getElementById("class-bt-dinamico").style.display = "none";
    document.getElementById("class-bt-download").style.display = "none";
}



