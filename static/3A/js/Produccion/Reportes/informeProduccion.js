const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');
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

selector_empaque.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
});

desde.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
});

hasta.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
});

const choiceEmpaques = new Choices('#selector_empaque', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE EMPAQUE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataDateTable = async () => {
    openLoading();

    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Empaque", getValueEmpaque());
        formData.append("Tipo", "TT");

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("data-informe/", options);
        const data = await response.json();

        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            if (!Array.isArray(data.DatosResumen) || data.DatosResumen.length === 0) {
                displayGeneral.style.visibility = 'hidden';
                mostrarInfo("No se encontraron datos para mostrar", "orange");
                closeLoading();
                return;
            }

            const tableData = data.DatosResumen.map((datos) => ({
                Lote: String(datos.Lote || ""),
                Productor: String(datos.Productor || ""),
                Especie: String(datos.Especie || ""),
                Variedad: String(datos.Variedad || ""),
                UMI: String(datos.UMI || ""),
                Kilos: String(datos.Kilos || ""),
                Calibre: String(datos.Calibre || ""),
                Envase: String(datos.Envase || ""),
                Marca: String(datos.Marca || ""),
                Calidad: String(datos.Calidad || ""),
                UP: String(datos.UP || ""),
                Embalador: String(datos.Embalador || ""),
                Clave: String(datos.Clave || ""),
                Cajas: String(datos.Cajas || ""),
                CantKilos: String(datos.CantKilos || ""),
                Empaque: String(datos.Empaque || ""),
                Descarte: String(datos.Descarte || ""),
                Pallet: String(datos.Pallet || ""),
                FechaPallet: String(datos.FechaPallet || ""),
                Fecha: String(datos.Fecha || ""),
                Hora: String(datos.Hora || "")
            }));
            const columnDefs = [
                { headerName: "LOTE", field: "Lote", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "PRODUCTOR", field: "Productor", filter: true, sortable: true, width: 150 },
                { headerName: "ESPECIE", field: "Especie", filter: true, sortable: true, width: 120 },
                { headerName: "VARIEDAD", field: "Variedad", filter: true, sortable: true, width: 120 },
                { headerName: "UMI", field: "UMI", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "KG", field: "Kilos", filter: true, sortable: true, width: 100, cellClass: 'cell-right' },
                { headerName: "CALIBRE", field: "Calibre", filter: true, sortable: true, width: 100, cellClass: 'cell-right' },
                { headerName: "ENVASE", field: "Envase", filter: true, sortable: true, width: 150 },
                { headerName: "MARCA", field: "Marca", filter: true, sortable: true, width: 150 },
                { headerName: "CALIDAD", field: "Calidad", filter: true, sortable: true, width: 120 },
                { headerName: "UP", field: "UP", filter: true, sortable: true, width: 100 },
                { headerName: "EMBALADOR", field: "Embalador", filter: true, sortable: true, width: 150 },
                { headerName: "CLAVE", field: "Clave", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CAJAS", field: "Cajas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CANT. KG", field: "CantKilos", filter: true, sortable: true, width: 120, cellClass: 'cell-right' },
                { headerName: "EMPAQUE", field: "Empaque", filter: true, sortable: true, width: 120 },
                { headerName: "DESCARTE", field: "Descarte", filter: true, sortable: true, width: 120, cellClass: 'cell-right' },
                { headerName: "PALLET", field: "Pallet", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "F. PALLET", field: "FechaPallet", filter: true, sortable: true, width: 120 },
                { headerName: "FECHA", field: "Fecha", filter: true, sortable: true, width: 120, cellClass: 'cell-center' },
                { headerName: "HORA", field: "Hora", filter: true, sortable: true, width: 120, cellClass: 'cell-center' }
            ];

            const gridDiv = document.getElementById('tableDataResumen');
            if (!gridDiv) {
                closeLoading();
                return;
            }
            gridDiv.innerHTML = '';
            if (typeof agGrid === 'undefined') {
                mostrarInfo("Error: La biblioteca de tabla no está disponible", "red");
                closeLoading();
                return;
            }

            try {
                gridOptions = {
                    columnDefs: columnDefs,
                    rowData: tableData,
                    pagination: true,
                    paginationPageSize: 50,
                    domLayout: 'autoHeight',
                    defaultColDef: {
                        resizable: true,
                        filter: true,
                        sortable: true
                    }
                };
                new agGrid.Grid(gridDiv, gridOptions);

                displayGeneral.style.visibility = 'visible';
                document.getElementById("class-bt-download").style.display = "block";
                mostrarInfo("Datos cargados correctamente", "green");
            } catch (gridError) {
                try {
                    gridOptions = {
                        columnDefs: columnDefs,
                        rowData: tableData
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
            }
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
    } finally {
        closeLoading();
    }
};

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
                    if (data.result && data.result.file_name) {
                        onComplete(data.result);
                    } else {
                        throw new Error("No se encontró el file_name en el resultado.");
                    }
                    hideInnerDescargaExcel();
                } else if (data.status === 'FAILURE') {
                    hideInnerDescargaExcel();
                    var nota = `La tarea falló: ${data.result.error.error_type} - ${data.result.error.error_message}`;
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


const descargarArchivo = async () => {
    showInnerDescargaExcel();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Empaque", getValueEmpaque());
        formData.append("Tipo", "TB");

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch('data-informe/', options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else {
            startPolling(data.TaskId, result => {
                if (result && result.file_name) {
                    const fileUrl = `archivo=${result.file_name}`;
                    window.location.href = fileUrl;
                } else {
                    throw new Error("No se encontró el file_name en el resultado.");
                }
            });



            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
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

function getValueEmpaque() {
    return choiceEmpaques.getValue() ? choiceEmpaques.getValue().value : '';
}

function showInnerDescargaExcel() {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor">
            <div class="imagen-tp-carga"></div>
            <p>El Archivo se descargará cuando esté listo, por favor no cierre esta pestaña.</p>
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
