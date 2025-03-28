const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');
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

document.getElementById('ver-dinamico-button').addEventListener('click', function () {
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

document.getElementById('busqueda-button').addEventListener('click', function () {
    if (!choiceCliente.getValue()) {
        mostrarInfo("Por favor, seleccione un Cliente.", "red");
    } else {
        dataDateTableTamaños();
    }
});

$(document).ready(function () {
    $('#tableDataBEA').DataTable({
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
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const dataDateTableTamaños = async () => {
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

        const response = await fetch("resumen-grilla-tamaños/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let datosTablaTamaño = ``;
            let datosTablaBEA = ``;
            data.DatosTamaño.forEach((datos) => {
                datosTablaTamaño += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda text-left">${datos.Variedad}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Kg}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Marca}</td>
                        <td class="pfa-tabla-celda text-rigth">${datos.TCajas}</td>
                        <td class="pfa-tabla-celda text-center">${datos._28_55}</td>
                        <td class="pfa-tabla-celda text-center">${datos._60_100}</td>
                        <td class="pfa-tabla-celda text-center">${datos._110}</td>
                        <td class="pfa-tabla-celda text-center">${datos._120}</td>
                        <td class="pfa-tabla-celda text-center">${datos._135_198}</td>
                    </tr>
                `
            });
            data.DatosBEA.forEach((datos) => {
                datosTablaBEA += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda text-left">${datos.Cliente}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Buque}</td>
                        <td class="pfa-tabla-celda text-center">${datos.ETD}</td>
                        <td class="pfa-tabla-celda text-center">${datos.FC}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Variedad}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Envase}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Marca}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Kg}</td>
                        <td class="pfa-tabla-celda text-center">${datos._28}</td>
                        <td class="pfa-tabla-celda text-center">${datos._60}</td>
                        <td class="pfa-tabla-celda text-center">${datos._70}</td>
                        <td class="pfa-tabla-celda text-center">${datos._80}</td>
                        <td class="pfa-tabla-celda text-center">${datos._90}</td>
                        <td class="pfa-tabla-celda text-center">${datos._100}</td>
                        <td class="pfa-tabla-celda text-center">${datos._110}</td>
                        <td class="pfa-tabla-celda text-center">${datos._120}</td>
                        <td class="pfa-tabla-celda text-center">${datos._135}</td>
                        <td class="pfa-tabla-celda text-center">${datos._150}</td>
                        <td class="pfa-tabla-celda text-center">${datos._163}</td>
                        <td class="pfa-tabla-celda text-center">${datos._175}</td>
                        <td class="pfa-tabla-celda text-center">${datos._198}</td>
                        <td class="pfa-tabla-celda text-right">${datos.I_Unit}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Total_FC}</td>
                        <td class="pfa-tabla-celda text-right">${datos._18Kg}</td>
                    </tr>
                `
            });
            if ($.fn.dataTable.isDataTable('#tableDataBEA')) {
                $('#tableDataBEA').DataTable().clear().destroy();
            }
            document.getElementById('beauty-total').innerHTML = `<strong class="beauty-total-strong">TOTAL CAJAS: ${data.TotalCajas}</strong>`;
            document.getElementById('beaty-cliente-nombre').innerHTML = `
                <span class="beauty-cliente-titulo">CLIENTE:</span>
                <span class="beauty-cliente-nombre">${getClienteSeleccionado()}</span>`;
            document.getElementById('pfa-tabla-DataResumen').innerHTML = datosTablaTamaño;
            document.getElementById('pfa-tabla-DataBEA').innerHTML = datosTablaBEA;
            dataTableAsignados = $('#tableDataBEA').DataTable({
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
                        "targets": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        "width": "3%"
                    },
                    {
                        "targets": [21, 22, 23],
                        "width": "3%"
                    },
                    {
                        "targets": [4, 5, 6],
                        "width": "6%"
                    },
                    {
                        "targets": [2, 3, 7],
                        "width": "3%"
                    },
                    {
                        "targets": [1],
                        "width": "12%"
                    }
                ]
            });
            jsonDatos = data.DatosProm;
            displayGeneral.style.visibility = 'visible';
            document.getElementById("class-bt-dinamico").style.display = "block";
            closeLoading();
        } else {
            document.getElementById("class-bt-dinamico").style.display = "none";
            displayGeneral.style.visibility = 'hidden';
            closeLoading();
            changeClean();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        displayGeneral.style.visibility = 'visible';
        document.getElementById("class-bt-dinamico").style.display = "none";
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};



const dataDateTableDynamic = async () => {
    try {
        $("#pivot-table").pivotUI(jsonDatos, {
            rows: ["Variedad", "Marca", "Calibre"],  // Variedad -> Marca -> Calibre
            cols: ["Semana", "Pais"],  // País -> Semana como columnas
            vals: ["Valor"],  // Usamos un valor derivado
            aggregatorName: "Sum",
            rendererName: "Table",
            derivedAttributes: {
                "Calibre": function (record) {
                    if (record["_28_55"] !== "0.00") return "28-55";
                    if (record["_60_100"] !== "0.00") return "60-100";
                    if (record["_110_125"] !== "0.00") return "110-125";
                    if (record["_135_198"] !== "0.00") return "135-198";
                    return "Sin Calibre";
                },
                "Valor": function (record) {
                    return parseFloat(record["_28_55"]) + parseFloat(record["_60_100"]) + parseFloat(record["_110_125"]) + parseFloat(record["_135_198"]);
                }
            },
            rendererOptions: {
                table: {
                    rowTotals: true,
                    colTotals: true
                }
            }
        });
        closeLoading();
    } catch (error) {
        closeLoading();
        mostrarInfo(`Se produjo un error: ${error}`, "red");
    }
};

const getClienteSeleccionado = () => {
    const value = choiceCliente.getValue(true);
    const option = document.querySelector(`#selector_cliente option[value="${value}"]`);
    return option.textContent;
}

function changeClean() {
    jsonDatos = null;
    document.getElementById("class-bt-dinamico").style.display = "none";
    displayGeneral.style.visibility = 'hidden';
    document.getElementById('beauty-total').innerHTML = ``;
    document.getElementById('pfa-tabla-DataResumen').innerHTML = ``;
    document.getElementById('pfa-tabla-DataBEA').innerHTML = ``;
    document.getElementById('beaty-cliente-nombre').innerHTML = ``;
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
            <a onclick="" style="display: none;">
                <i class='bx material-symbols-outlined icon'>download</i>
            </a>
            </div>
        </div>
    `;
    document.querySelector('.pop-all-overlay').style.display = 'flex';
}