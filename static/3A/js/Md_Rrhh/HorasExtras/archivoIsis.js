document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    dataInicial();
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    dataDateTable();
});

document.getElementById('exportar-button').addEventListener('click', function () {
    showPopDescarga();
});

desde.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
});

hasta.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
})


selector_centros.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
    dataSubItems();
});

const choiceCentro = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CENTRO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});
const choiceLegajo = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE LEGAJO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("data-inicial/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });

            choiceCentro.clearChoices();
            choiceCentro.removeActiveItems();

            choiceCentro.setChoices(result, 'value', 'label', true);
        } else {
            choiceCentro.clearChoices();
            choiceCentro.removeActiveItems();
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

const dataSubItems = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Centro", getValueCentro());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("sub-data/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [{ value: '', label: 'TODO' }];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Codigo, label: datos.Descripcion });
            });
            choiceLegajo.clearChoices();
            choiceLegajo.removeActiveItems();
            choiceLegajo.setChoices(result, 'value', 'label', true);
        } else {
            choiceLegajo.clearChoices();
            choiceLegajo.removeActiveItems();
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
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Centro", getValueCentro());
        formData.append("Legajo", getValueLegajo());
        formData.append("Archivo", 'N');

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("listar-data/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            jsonData = data.Datos;

            if (!Array.isArray(jsonData) || jsonData.length === 0) {
                displayGeneral.style.visibility = 'hidden';
                mostrarInfo("No se encontraron datos para mostrar", "orange");
                return;
            }

            const tableData = jsonData.map((datos) => ({
                Legajo: String(datos.Legajo || ""),
                Nombre: String(datos.Nombre || ""),
                Centro: String(datos.Centro || ""),
                Sindicato: String(datos.Sindicato || ""),
                Horas50: String(datos.Horas50 || ""),
                Horas100: String(datos.Horas100 || ""),
                HorasS: String(datos.HorasS || ""),
                Acuerdo50: String(datos.Ac50 || ""),
                Acuerdo100: String(datos.Ac100 || ""),
            }));

            const columnDefs = [
                { headerName: "LEGAJO", field: "Legajo", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "APELLIDO Y NOMBRE", field: "Nombre", filter: true, sortable: true, width: 300, cellClass: 'cell-left' },
                { headerName: "CENTRO DE COSTO", field: "Centro", filter: true, sortable: true, width: 170, cellClass: 'cell-center' },
                { headerName: "SINDICATO", field: "Sindicato", filter: true, sortable: true, width: 170, cellClass: 'cell-left' },
                { headerName: "HORAS 50%", field: "Horas50", filter: true, sortable: true, width: 170, cellClass: 'cell-center' },
                { headerName: "HORAS 100%", field: "Horas100", filter: true, sortable: true, width: 170, cellClass: 'cell-center' },
                { headerName: "HORAS SIMPLES", field: "HorasS", filter: true, sortable: true, width: 170, cellClass: 'cell-center' },
                { headerName: "ACUERDO 50%", field: "Acuerdo50", filter: true, sortable: true, width: 170, cellClass: 'cell-center' },
                { headerName: "ACUERDO 100%", field: "Acuerdo100", filter: true, sortable: true, width: 170, cellClass: 'cell-center' }
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
                    rowHeight: 30,
                    headerHeight: 32,
                    columnDefs: columnDefs,
                    rowData: tableData,
                    floatingFilter: true,
                    quickFilterText: '',
                    defaultColDef: {
                        resizable: true
                    },
                    onGridReady: function (params) {
                        params.api.sizeColumnsToFit();
                    }
                };

                gridDiv.classList.add("ag-theme-alpine");
                const gridApi = agGrid.createGrid(gridDiv, gridOptions);
                if (gridApi) {
                    gridOptions.api = gridApi;
                }

                displayGeneral.style.visibility = 'visible';
            } catch (alternativeError) {
                mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
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

const descargaExcel = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", fechaIsisDesde());
        formData.append("Final", fechaIsisHasta());
        formData.append("Centro", '');
        formData.append("Legajo", '');
        formData.append("Archivo", 'S');

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("listar-data/", options);
        const contentType = response.headers.get('content-type');

        if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            const blob = await response.blob();
            const excelURL = URL.createObjectURL(blob);
            window.open(excelURL);
            hiddenInnerPop();
        } else {
            const data = await response.json();
            if (data.Message == "Not Authenticated") {
                window.location.href = data.Redirect;
            } else {
                var nota = data.Nota || data.Message;
                var color = "red";
                mostrarInfo(nota, color);
            }
        }
    } catch (error) {
        const nota = "Se produjo un error al procesar la solicitud. " + error.message;
        const color = "red";
        mostrarInfo(nota, color);
    }  finally {
        closeLoading();
    }
};











































































function fechaIsisDesde() {
    return document.getElementById('desde-isis').value;
}

function fechaIsisHasta() {
    return document.getElementById('hasta-isis').value;
}

function Inicio() {
    const fechaDesde = document.getElementById('vr-fecha-desde').value;
    return fechaDesde;
}

function Final() {
    const fechaHasta = document.getElementById('vr-fecha-hasta').value;
    return fechaHasta;
}

function getValueCentro() {
    return choiceCentro.getValue() ? choiceCentro.getValue().value : '';
}

function getValueLegajo() {
    return choiceLegajo.getValue() ? choiceLegajo.getValue().value : '';
}

function showPopDescarga() {

    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor" style="border: 1px solid #ccc; margin-top: 5px; width: 400px;">
            <p>ARCHIVO ISIS</p>
            <div class="vr-fila-5">
                <div class="vr-col-6">
                    <div>
                        <span>Desde:</span>
                        <input type="date" onclick="this.showPicker();" id="desde-isis" class="vr-input" value="${Inicio()}">
                    </div>
                </div>
                <div class="vr-col-6">
                    <div>
                        <span>Hasta:</span>
                        <input type="date" onclick="this.showPicker();" id="hasta-isis" class="vr-input" value="${Final()}">
                    </div>
                </div>
            </div>
        </div>
        <div class="carga-contenedor" style="text-align: center; margin-top: 10px;">
            <div class="vr-fila-2" style="gap: 25px;">
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="hiddenInnerPop();" id="cancelar-descarga-button">CANCELAR</button>
                </div>
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="descargaExcel();" id="descargar-subir-button">DESCARGAR</button>
                </div>
            </div>
        </div>
    `;
    document.getElementById("fondo-oscuro").style.display = "block";
    document.getElementById("popup-confirmacion").style.display = "block";
}

function hiddenInnerPop() {
    document.getElementById('contenido-popup').innerHTML = ``;
    document.getElementById("fondo-oscuro").style.display = "none";
    document.getElementById("popup-confirmacion").style.display = "none";
}

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
