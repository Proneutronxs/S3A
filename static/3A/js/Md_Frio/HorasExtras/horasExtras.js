document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    displayGeneral.style.visibility = 'hidden';
    dataInicial();
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    changeClean();
    dataDateTable();
});

document.getElementById('autorizar-button').addEventListener('click', function () {
    envia_horas('G');
});

document.getElementById('eliminar-button').addEventListener('click', function () {
    envia_horas('E');
});

selector_centro.addEventListener("change", (event) => {
    changeClean();
    dataPersonal();
});

selector_estado.addEventListener("change", (event) => {
    changeClean();
});

selector_personal.addEventListener("change", (event) => {
    changeClean();
});

desde.addEventListener("change", (event) => {
    changeClean();
});

hasta.addEventListener("change", (event) => {
    changeClean();
});

const choiceCentros = new Choices('#selector_centro', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CENTRO DE COSTO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEstado = new Choices('#selector_estado', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ESTADO HORA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choicePersonal = new Choices('#selector_personal', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE PERSONAL',
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
        const response = await fetch("data-inicial/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push({ value: '', label: 'TODOS' });
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.IdCentro, label: datos.Descripcion
                });
            });
            choiceCentros.setChoices(result, 'value', 'label', true);


            let result2 = [];
            result2.push();
            data.Estados.forEach((datos) => {
                result2.push({
                    value: datos.IdEstado, label: datos.Descripcion
                });
            });
            choiceEstado.setChoices(result2, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const dataPersonal = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Centro", getValueCentros());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("personal-centro/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choicePersonal.clearChoices();
            choicePersonal.removeActiveItems();
            choicePersonal.setChoices(result, 'value', 'label', true);
        } else {
            choicePersonal.clearChoices();
            choicePersonal.removeActiveItems();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
        closeLoading();
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
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Estado", getValueEstado());
        formData.append("Legajo", getValuePersonal());
        formData.append("Centro", getValueCentros());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listado-data/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {

            if ($.fn.dataTable.isDataTable('#tableDataCuentas')) {
                $('#tableDataCuentas').DataTable().clear().destroy();
            }

            let datosTabla = ``;
            data.Datos.forEach((datos) => {
                datosTabla += `
                <tr class="pfa-tabla-fila">
                    <td class="cell-center">
                        <input class="input-checkbox-hs checkbox" type="checkbox" name="idCheck" value="${datos.ID_HEP}" ${datos.Estado === '0' ? 'disabled' : ''}>
                    </td>
                    <td class="cell-center">
                        <select class="choices_inner vr-select" style="width: 85px;" name="tipoHoraExtra">
                            <option value="A" ${datos.Tipo === 'A' ? 'selected' : ''}>A</option>
                            <option value="50" ${datos.Tipo === '50' ? 'selected' : ''}>50</option>
                            <option value="100" ${datos.Tipo === '100' ? 'selected' : ''}>100</option>
                            <option value="N" ${datos.Tipo === 'N' ? 'selected' : ''}>N</option>
                            <option value="AC-50" ${datos.Tipo === 'AC-50' ? 'selected' : ''}>AC 50</option>
                            <option value="AC-100" ${datos.Tipo === 'AC-100' ? 'selected' : ''}>AC 100</option>
                        </select>
                    </td>
                    <td class="cell-center">${datos.Legajo}</td>
                    <td class="cell-left">${datos.Nombre}</td>
                    <td class="cell-left">${datos.Centro}</td>
                    <td>${datos.Desde}</td>
                    <td>${datos.Hasta}</td>
                    <td class="cell-center">
                        <input class="new-vr-select" type="number" name="cantHoras" step="0.5" style="max-width: 80px;" value="${datos.Cantidad}">
                    </td>
                    <td class="cell-left">${datos.Motivo}</td>
                    <td class="cell-left">${datos.Descripcion}</td>
                    <td class="cell-left">${datos.Solicita}</td>
                    <td class="cell-center">${datos.E}</td>
                </tr>
                `
            });
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
                        "targets": [0, 1, 2, 7, 8],
                        "width": "1%",
                    },
                    {
                        "targets": [3, 4],
                        "width": "13%",
                    }
                ]
            });
            $("#selectAll").on("change", function () {
                const isChecked = $(this).prop("checked");
                $('#tableDataCuentas tbody input[type="checkbox"]:not([disabled])').prop("checked", isChecked);
            });
            $(document).on("change", '#tableDataCuentas tbody input[type="checkbox"]', function () {
                const allChecked = $('#tableDataCuentas tbody input[type="checkbox"]:not([disabled])').length ===
                    $('#tableDataCuentas tbody input[type="checkbox"]:not([disabled]):checked').length;
                $("#selectAll").prop("checked", allChecked);
            });
            displayGeneral.style.visibility = 'visible';
        } else {
            displayGeneral.style.visibility = 'hidden';
            document.getElementById('pfa-tabla-DataCuentas').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
        closeLoading();
    } catch (error) {
        displayGeneral.style.visibility = 'hidden';
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const envia_horas = async (metodo) => {
    openLoading();
    try {
        const selectedRows = [];

        $('#tableDataCuentas tbody input[type="checkbox"]:checked').each(function () {
            const row = $(this).closest('tr');
            const tipoHora = row.find('select[name="tipoHoraExtra"]').val();
            const cantidad = parseFloat(row.find('input[name="cantHoras"]').val()) || 0;
            selectedRows.push({
                IDHEP: row.find('input[name="idCheck"]').val(),
                tipoHora: tipoHora,
                cantidad: cantidad
            });
        });
        if (selectedRows.length === 0) {
            mostrarInfo("Por favor, seleccione al menos una fila", "orange");
            closeLoading();
            return;
        }

        displayGeneral.style.visibility = 'hidden';
        const formData = new FormData();
        formData.append("Metodo", metodo);
        selectedRows.forEach((row, index) => {
            formData.append(`IDhep${index}`, row.IDHEP);
            formData.append(`TipoHoraExtra${index}`, row.tipoHora);
            formData.append(`CantidadHoras${index}`, row.cantidad);
        });
        formData.append("IDHEP", selectedRows.length);

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("enviar-horas/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            dataDateTable();
            document.getElementById('selectAll').checked = false;
            mostrarInfo(data.Nota, "green");
        } else {
            dataDateTable();
            mostrarInfo(data.Nota, "red");
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};



function getValuePersonal() {
    return choicePersonal.getValue() ? choicePersonal.getValue().value : '';
}

function getValueCentros() {
    return choiceCentros.getValue() ? choiceCentros.getValue().value : '';
}

function getValueEstado() {
    return choiceEstado.getValue() ? choiceEstado.getValue().value : '3';
}

function changeClean() {
    displayGeneral.style.visibility = 'hidden';
}

function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    let mesDesde = mes - 1;
    let anoDesde = ano;
    if (mesDesde < 1) {
        mesDesde = 12;
        anoDesde = ano - 1;
    }
    const formattedDateDesde = `${anoDesde}-${String(mesDesde).padStart(2, '0')}-${'01'}`;
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