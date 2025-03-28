const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    changeClean();
    fechaActual();
});

selector_tipo.addEventListener("change", (event) => {
    changeClean();
});

desde.addEventListener("change", (event) => {
    changeClean();
});

hasta.addEventListener("change", (event) => {
    changeClean();
});

const choiceTipo = new Choices('#selector_tipo', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE TIPO DE CUENTA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

// const choiceSubCliente = new Choices('#selector_sub_cliente', {
//     allowHTML: true,
//     shouldSort: false,
//     placeholderValue: 'SELECCIONE CLIENTE',
//     searchPlaceholderValue: 'Escriba para buscar..',
//     itemSelectText: ''
// });

document.getElementById('busqueda-button').addEventListener('click', function () {
    if (!choiceTipo.getValue()) {
        mostrarInfo("Por favor, seleccione tipo de cuenta.", "red");
    } else {
        dataDateTable();
    }
});

$(document).ready(function () {
    $('#tableDataResumen').DataTable({
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

// const dataInicial = async () => {
//     openLoading();
//     try {
//         const response = await fetch("clientes-principales/");
//         const data = await response.json();
//         closeLoading();
//         if (data.Message === "Success") {
//             let result = [];
//             result.push();
//             data.Datos.forEach((datos) => {
//                 result.push({
//                     value: datos.IdCuenta, label: datos.Descripcion,
//                     customProperties: JSON.stringify({ Principal: datos.Principal })
//                 });
//             });
//             choiceCliente.setChoices(result, 'value', 'label', true);
//         } else {
//             var nota = data.Nota
//             var color = "red";
//             mostrarInfo(nota, color);
//         }
//     } catch (error) {
//         closeLoading();
//         var nota = "Se produjo un error al procesar la solicitud. " + error;
//         var color = "red";
//         mostrarInfo(nota, color);
//     }
// }

// const dataSubItems = async () => {
//     openLoading();
//     try {
//         const formData = new FormData();
//         formData.append("IdCliente", getValuePSubCliente());
//         const options = {
//             method: 'POST',
//             headers: {
//             },
//             body: formData
//         };

//         const response = await fetch("sub-clientes/", options);
//         const data = await response.json();
//         if (data.Message == "Not Authenticated") {
//             window.location.href = data.Redirect;
//         } else if (data.Message == "Success") {
//             let result = [];
//             result.push();
//             data.Datos.forEach((datos) => {
//                 result.push({ value: datos.IdCuenta, label: datos.Descripcion });
//             });
//             choiceSubCliente.clearChoices();
//             choiceSubCliente.removeActiveItems();
//             choiceSubCliente.setChoices(result, 'value', 'label', true);
//         } else {
//             choiceSubCliente.clearChoices();
//             choiceSubCliente.removeActiveItems();
//         }
//         closeLoading();
//     } catch (error) {
//         closeLoading();
//         var nota = "Se produjo un error al procesar la solicitud. " + error;
//         var color = "red";
//         mostrarInfo(nota, color);
//     }
// };

const dataDateTable = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCliente", '');
        formData.append("IdSubCliente", '');
        formData.append("TipoCte", getValueTipoCliente());
        formData.append("Tipo", "TT");
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("resumen-cuentas/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let datosTabla = ``;
            data.DatosResumen.forEach((datos) => {
                datosTabla += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda text-left">${datos.Cliente}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Pais}</td>
                        <td class="pfa-tabla-celda text-center">${datos.CantFC}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Pallets}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Box9}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Box15}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Box18}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Box22}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Cantidad}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Promedio18}</td>
                        <td class="pfa-tabla-celda text-right">${datos.TotalFC}</td>
                        <td class="pfa-tabla-celda text-right">${datos.TotalNC}</td>
                        <td class="pfa-tabla-celda text-right">${datos.TotalNeto}</td>
                        <td class="pfa-tabla-celda text-right">${datos.TotalCancel}</td>
                        <td class="pfa-tabla-celda text-right">${datos.TotalPendiente}</td>
                        <td class="pfa-tabla-celda text-right">${datos.AveragePrice}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Comm1}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Comm2}</td>
                    </tr>
                `
            });
            const totales = data.Totales[0];
            document.getElementById("tfoot-DataTotales").innerHTML = `
                <tr class="pfa-tabla-fila total-row">
                    <td class="pfa-tabla-encabezado-celda"><strong> </strong></td>
                    <td class="pfa-tabla-encabezado-celda"><strong>TOTALES: </strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.CantFC}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Pallets}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Box9}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Box15}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Box18}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Box22}</strong></td>
                    <td class="pfa-tabla-celda text-center"><strong>${totales.Cantidad}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.Promedio18}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.TotalFC}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.TotalNC}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.TotalNeto}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.TotalCancel}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.TotalPendiente}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.AveragePrice}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.Comm1}</strong></td>
                    <td class="pfa-tabla-celda text-right"><strong>${totales.Comm2}</strong></td>
                </tr>
            `;

            if ($.fn.dataTable.isDataTable('#tableDataResumen')) {
                $('#tableDataResumen').DataTable().clear().destroy();
            }


            document.getElementById('pfa-tabla-DataResumen').innerHTML = datosTabla;
            dataTableAsignados = $('#tableDataResumen').DataTable({
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
                        "targets": [16,17],
                        "width": "1%"
                    },
                    {
                        "targets": [0],
                        "width": "15%"
                    },
                    {
                        "targets": [1],
                        "width": "6%"
                    },
                    // {
                    //     "targets": [2,3,4,5,6,7,8,9],
                    //     "width": "5%"
                    // },
                    {
                        "targets": [10,11,12,13,14,15],
                        "width": "6%"
                    }
                ]
            });
            displayGeneral.style.visibility = 'visible';
            document.getElementById("class-bt-download").style.display = "block";
        } else {
            document.getElementById('pfa-tabla-DataResumen').innerHTML = ``;
            displayGeneral.style.visibility = 'hidden';
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


const descargarArchivo = async (name) => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCliente", '');
        formData.append("IdSubCliente", '');
        formData.append("TipoCte", getValueTipoCliente());
        formData.append("Tipo", "TB");

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch('resumen-cuentas/', options);
        const contentType = response.headers.get('content-type');
        closeLoading();
        if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            const blob = await response.blob();
            const excelURL = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = excelURL;
            a.style.display = 'none';
            a.download = 'Resumen_Cuentas_' + obtenerFechaHoraActual() + '.xlsx';
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


// function getValueCliente() {
//     return choiceCliente.getValue() ? choiceCliente.getValue().value : '';
// }

// function getValuePSubCliente() {
//     const selectedValue = choiceCliente.getValue();
//     if (selectedValue) {
//         const customProperties = JSON.parse(selectedValue.customProperties);
//         return customProperties.Principal;
//     }
//     return '';
// }

function getValueTipoCliente() {
    return choiceTipo.getValue() ? choiceTipo.getValue().value : '';
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

function changeClean() {
    displayGeneral.style.visibility = 'hidden';
    // document.getElementById('beauty-total').innerHTML = ``;
    // document.getElementById('pfa-tabla-DataResumen').innerHTML = ``;
    // document.getElementById('pfa-tabla-DataBEA').innerHTML = ``;
    // document.getElementById('beaty-cliente-nombre').innerHTML = ``;
}
