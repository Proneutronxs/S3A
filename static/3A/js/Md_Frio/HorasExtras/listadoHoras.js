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

document.getElementById('class-bt-download').addEventListener('click', function () {
    descarga_archivo();
});

selector_centros.addEventListener("change", (event) => {
    changeClean();
    dataPersonal();
});

selector_personal.addEventListener("change", (event) => {
    changeClean();
});

selector_estado.addEventListener("change", (event) => {
    changeClean();
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CENTRO DE COSTO',
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

const choiceEstado = new Choices('#selector_estado', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ESTADO HORA',
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

            let result2 = [{value: '', label: 'TODO'}, {value: '0', label: 'AUTORIZADO'}, {value: '8', label: 'ELIMINADO'}, {value: '3', label: 'PENDIENTE'}];
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
        formData.append("Centro", getValueCentros());
        formData.append("Legajo", getValuePersonal());
        formData.append("Estado", getValueEstado());
        formData.append("Archivo", 'N');
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("reporte-web/", options);
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
                    <td class="cell-center">${datos.Tipo}</td>
                    <td class="cell-center">${datos.Legajo}</td>
                    <td class="cell-left">${datos.Nombre}</td>
                    <td class="cell-left">${datos.Centro}</td>
                    <td class="cell-center">${datos.Desde}</td>
                    <td class="cell-center">${datos.Hasta}</td>
                    <td class="cell-center">${datos.Cantidad}</td>
                    <td class="cell-left">${datos.Motivo}</td>
                    <td class="cell-left">${datos.Descripcion}</td>
                    <td class="cell-left">${datos.Solicita}</td>
                    <td class="cell-center">${datos.Estado}</td>
                    <td class="cell-center">${datos.Dispositivo}</td>
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
                        "targets": [0, 1, 4, 5, 6],
                        "width": "5%",
                    },
                    {
                        "targets": [2, 3],
                        "width": "13%",
                    }
                ]
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

const descarga_archivo = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Centro", getValueCentros());
        formData.append("Legajo", getValuePersonal());
        formData.append("Estado", getValueEstado());
        formData.append("Archivo", 'S');
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("reporte-web/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            window.location.href = 'archivo='+data.Archivo;
        } else {
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


























































function getValuePersonal() {
    return choicePersonal.getValue() ? choicePersonal.getValue().value : '';
}

function getValueCentros() {
    return choiceCentros.getValue() ? choiceCentros.getValue().value : '';
}

function getValueEstado() {
    return choiceEstado.getValue() ? choiceEstado.getValue().value : '';
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