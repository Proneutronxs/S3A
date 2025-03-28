const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');
let jsonData;
let gridOptions;
let statusInterval;


window.addEventListener("load", async () => {
    displayGeneral.style.visibility = 'hidden';
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    dataDateTable();
});

document.getElementById('class-bt-download').addEventListener('click', function () {
    descargarArchivo();
});

// selector_especie.addEventListener("change", (event) => {
//     displayGeneral.style.visibility = 'hidden';
// });

// selector_variedad.addEventListener("change", (event) => {
//     displayGeneral.style.visibility = 'hidden';
// });

desde.addEventListener("change", (event) => {
    document.getElementById("class-bt-download").style.display = "none";
    displayGeneral.style.visibility = 'hidden';
});

hasta.addEventListener("change", (event) => {
    document.getElementById("class-bt-download").style.display = "none";
    displayGeneral.style.visibility = 'hidden';
});

// const choiceEspecie = new Choices('#selector_especie', {
//     allowHTML: true,
//     shouldSort: false,
//     placeholderValue: 'SELECCIONE ESPECIE',
//     searchPlaceholderValue: 'Escriba para buscar..',
//     itemSelectText: ''
// });

// const choiceVariedad = new Choices('#selector_variedad', {
//     allowHTML: true,
//     shouldSort: false,
//     placeholderValue: 'SELECCIONE VARIEDAD',
//     searchPlaceholderValue: 'Escriba para buscar..',
//     itemSelectText: ''
// });

async function checkTaskStatus(taskId) {
    try {
        const response = await fetch(`status_worker_celery/${taskId}`);
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Error al verificar el estado de la tarea: ' + error.message);
    }
}

function startPolling(taskId, onComplete, interval = 5000) {
    const poll = () => {
        checkTaskStatus(taskId)
            .then(data => {
                if (data.status === 'SUCCESS') {
                    onComplete(data.result);
                    hideInnerDescargaExcel();
                } else if (data.status === 'FAILURE') {
                    hideInnerDescargaExcel();
                    var nota = `La tarea falló: ${data.error.error_type} - ${data.error.error_message}`;
                    mostrarInfo(nota, 'red');
                } else {
                    setTimeout(() => poll(), interval);
                }
            })
            .catch(error => {
                var nota = 'Error al verificar el estado: ' + error.message;
                mostrarInfo(nota, 'red');
                hideInnerDescargaExcel();
            });
    };
    poll();
}

const dataDateTable = async () => {
    showInnerDescargaExcel("La Informacion se mostrará cuando esté disponible, por favor no cierre esta pestaña.");
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Empaque", '');
        formData.append("Tipo", "TT");

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("data-pallets/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            startPolling(data.TaskId, result => {
                if (result && result.ListaDatos) {
                    jsonData = result.ListaDatos;
                    if (!Array.isArray(jsonData) || jsonData.length === 0) {
                        displayGeneral.style.visibility = 'hidden';
                        mostrarInfo("No se encontraron datos para mostrar", "orange");
                        return;
                    }

                    const tableData = jsonData.map((datos) => ({
                        Deposito: String(datos.Deposito || ""),
                        Clave: String(datos.Clave || ""),
                        DescripcionClave: String(datos.DescripcionClave || ""),
                        Especie: String(datos.Especie || ""),
                        Variedad: String(datos.Variedad || ""),
                        Calidad: String(datos.Calidad || ""),
                        Marca: String(datos.Marca || ""),
                        Envase: String(datos.Envase || ""),
                        Papel: String(datos.Papel || ""),
                        Tratamiento: String(datos.Tratamiento || ""),
                        NroPallet: String(datos.NroPallet || ""),
                        FechaPallet: String(datos.FechaPallet || ""),
                        Mes: String(datos.Mes || ""),
                        Dia: String(datos.Dia || ""),
                        PalId: String(datos.PalId || ""),
                        PrId: String(datos.PrId || ""),
                        ProductoId: String(datos.ProductoId || ""),
                        ProductoDesc: String(datos.ProductoDesc || ""),
                        Total: String(datos.Total || ""),
                        Lugar: String(datos.Lugar || ""),
                        Valor1: String(datos.Valor1 || ""),
                        Valor2: String(datos.Valor2 || ""),
                        Valor3: String(datos.Valor3 || ""),
                        Valor4: String(datos.Valor4 || ""),
                        Valor5: String(datos.Valor5 || ""),
                        Valor6: String(datos.Valor6 || ""),
                        Valor7: String(datos.Valor7 || ""),
                        Valor8: String(datos.Valor8 || ""),
                        Valor9: String(datos.Valor9 || ""),
                        Valor10: String(datos.Valor10 || ""),
                        Valor11: String(datos.Valor11 || ""),
                        Valor12: String(datos.Valor12 || ""),
                        Valor13: String(datos.Valor13 || ""),
                        LuId: String(datos.LuId || ""),
                        NPallet: String(datos.NPallet || ""),
                        Alias: String(datos.Alias || ""),
                        Producto: String(datos.Producto || ""),
                        Unidad: String(datos.Unidad || ""),
                        PuntoControl: String(datos.PuntoControl || ""),
                        Obs: String(datos.Obs || ""),
                        PrDestino: String(datos.PrDestino || ""),
                        PrConservacion: String(datos.PrConservacion || ""),
                        ConSec: String(datos.ConSec || ""),
                        StatusCal: String(datos.StatusCal || ""),
                        CajaXPallet: String(datos.CajaXPallet || ""),
                        PalStatus: String(datos.PalStatus || ""),
                        Peso: String(datos.Peso || ""),
                        Plu: String(datos.Plu || ""),
                        Pallets: String(datos.Pallets || ""),
                        Conservacion: String(datos.Conservacion || ""),
                    }));

                    const columnDefs = [
                        { headerName: "DEPÓSITO", field: "Deposito", filter: true, sortable: true, width: 150 },
                        { headerName: "CLAVE", field: "Clave", filter: true, sortable: true, width: 100 },
                        { headerName: "DESC. CLAVE", field: "DescripcionClave", filter: true, sortable: true, width: 150 },
                        { headerName: "ESPECIE", field: "Especie", filter: true, sortable: true, width: 120 },
                        { headerName: "VARIEDAD", field: "Variedad", filter: true, sortable: true, width: 120 },
                        { headerName: "CALIDAD", field: "Calidad", filter: true, sortable: true, width: 120 },
                        { headerName: "MARCA", field: "Marca", filter: true, sortable: true, width: 150 },
                        { headerName: "ENVASE", field: "Envase", filter: true, sortable: true, width: 120 },
                        { headerName: "PAPEL", field: "Papel", filter: true, sortable: true, width: 120 },
                        { headerName: "TRATAMIENTO", field: "Tratamiento", filter: true, sortable: true, width: 150 },
                        { headerName: "N° PALLET", field: "NroPallet", filter: true, sortable: true, width: 120 },
                        { headerName: "FECHA PALLET", field: "FechaPallet", filter: true, sortable: true, width: 150 },
                        { headerName: "MES", field: "Mes", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "DÍA", field: "Dia", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "PALLET ID", field: "PalId", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "PR ID", field: "PrId", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "PRODUCTO ID", field: "ProductoId", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "PRODUCTO DESC", field: "ProductoDesc", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "TOTAL", field: "Total", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "LUGAR", field: "Lugar", filter: true, sortable: true, width: 150 },
                        { headerName: "28", field: "Valor1", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "60", field: "Valor2", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "70", field: "Valor3", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "80", field: "Valor4", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "88", field: "Valor5", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "100", field: "Valor6", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "113", field: "Valor7", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "125", field: "Valor8", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "138", field: "Valor9", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "150", field: "Valor10", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "163", field: "Valor11", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "175", field: "Valor12", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "198", field: "Valor13", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                        { headerName: "LUGAR ID", field: "LuId", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "N° Pallet", field: "NPallet", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "ALIAS", field: "Alias", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                        { headerName: "PRODUCTO", field: "Producto", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                        { headerName: "UNIDAD", field: "Unidad", filter: true, sortable: true, width: 150 },
                        { headerName: "PUNTO CONTROL", field: "PuntoControl", filter: true, sortable: true, width: 150 },
                        { headerName: "OBSERVACION", field: "Obs", filter: true, sortable: true, width: 150 },
                        { headerName: "PR DESTINO", field: "PrDestino", filter: true, sortable: true, width: 150 },
                        { headerName: "PR CONSERVACION", field: "PrConservacion", filter: true, sortable: true, width: 150 },
                        { headerName: "CON SEC", field: "ConSec", filter: true, sortable: true, width: 150 },
                        { headerName: "STATUS CAL", field: "StatusCal", filter: true, sortable: true, width: 150 },
                        { headerName: "CAJAS x PALLET", field: "CajaXPallet", filter: true, sortable: true, width: 150 },
                        { headerName: "PALLET STATUS", field: "PalStatus", filter: true, sortable: true, width: 110, cellClass: 'cell-center' },
                        { headerName: "PESO", field: "Peso", filter: true, sortable: true, width: 150 },
                        { headerName: "PLU", field: "Plu", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                        { headerName: "PALLETS", field: "Pallets", filter: true, sortable: true, width: 150 }
                    ];

                    const gridDiv = document.getElementById('tableDataResumen');
                    if (!gridDiv) {
                        return;
                    }
                    gridDiv.innerHTML = '';
                    if (typeof agGrid === 'undefined') {
                        mostrarInfo("Error: La biblioteca de tabla no está disponible", "red");
                        return;
                    }

                    try {
                        gridOptions = {
                            columnDefs: columnDefs,
                            rowData: tableData,
                            floatingFilter: true,
                            quickFilterText: ''
                        };

                        gridDiv.classList.add("ag-theme-alpine");
                        const gridApi = agGrid.createGrid(gridDiv, gridOptions);
                        if (gridApi) {
                            gridOptions.api = gridApi;
                        }
                        displayGeneral.style.visibility = 'visible';
                        document.getElementById("class-bt-download").style.display = "block";
                    } catch (alternativeError) {
                        mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
                    }
                } else {
                    throw new Error("No se encontró el resultado.");
                }
            });
        } else {
            displayGeneral.style.visibility = 'hidden';
            const nota = data.Nota || "No se pudo cargar la información";
            const color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        const nota = "Se produjo un error al procesar la solicitud. " + error.message;
        const color = "red";
        mostrarInfo(nota, color);
    }
};

const descargarArchivo = async () => {
    showInnerDescargaExcel("El Excel se descargará cuando esté disponible, por favor no cierre esta pestaña.");
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Tipo", "TB");

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch('data-pallets/', options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else {
            startPolling(data.TaskId, result => {
                if (result && result.file_name) {
                    if (result.file_name == 'e') {
                        throw new Error("No se encontró el archivo en el resultado.");
                    } else {
                        hideInnerDescargaExcel();
                        const fileUrl = `archivo=${result.file_name}`;
                        window.location.href = fileUrl;
                    }
                } else {
                    throw new Error("No se encontró el archivo en el resultado.");
                }
            });
        }
    } catch (error) {
        hideInnerDescargaExcel();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
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


function showInnerDescargaExcel(texto) {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor">
            <div class="imagen-tp-carga"></div>
            <p>${texto}</p>
        </div>
        <div class="carga-contenedor">
            <div class="carga">
                <div class="punto-carga"></div>
                <div class="punto-carga"></div>
                <div class="punto-carga"></div>
            </div>
        </div>
    `;
    document.getElementById("fondo-oscuro").style.display = "block";
    document.getElementById("popup-confirmacion").style.display = "block";
}

function hideInnerDescargaExcel() {
    document.getElementById('contenido-popup').innerHTML = `
    `;
    document.getElementById("fondo-oscuro").style.display = "none";
    document.getElementById("popup-confirmacion").style.display = "none";
}
