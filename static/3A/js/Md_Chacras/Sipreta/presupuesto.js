document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    dataInicial();
});

selector_productores.addEventListener("change", (event) => {
    changeClean();
    dataSubItems();
});

selector_chacras.addEventListener("change", (event) => {
    changeClean();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    if (!choiceProductores.getValue()) {
        mostrarInfo("Por favor, seleccione un Productor.", "red");
    } else {
        dataDateTable();
    }
});

document.getElementById('class-bt-upload').addEventListener('click', function () {
    showInnerSubirExcel('Subir datos a ' + getLabelChacra());
});

const choiceProductores = new Choices('#selector_productores', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE PRODUCTOR',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceChacras = new Choices('#selector_chacras', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CHACRA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("combox-productores/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.IdProductor, label: datos.Descripcion
                });
            });
            choiceProductores.setChoices(result, 'value', 'label', true);
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

const dataSubItems = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdProductor", getValuesProductor());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("combox-chacras/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.IdChacra, label: datos.Descripcion });
            });
            choiceChacras.clearChoices();
            choiceChacras.removeActiveItems();
            choiceChacras.setChoices(result, 'value', 'label', true);
        } else {
            choiceChacras.clearChoices();
            choiceChacras.removeActiveItems();
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
        formData.append("IdProductor", getValuesProductor());
        formData.append("IdChacra", getValuesChacra());
        formData.append("Tipo", "TT");

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("data-listado/", options);
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
                IdProductor: String(datos.IdProductor || ""),
                Productor: String(datos.Productor || ""),
                IdChacra: String(datos.IdChacra || ""),
                Chacra: String(datos.Chacra || ""),
                Cuadro: String(datos.Cuadro || ""),
                Fila: String(datos.Fila || ""),
                IdEspecie: String(datos.IdEspecie || ""),
                Especie: String(datos.Especie || ""),
                IdVariedad: String(datos.IdVariedad || ""),
                Variedad: String(datos.Variedad || ""),
                AñoPlantacion: String(datos.AñoPlantacion || ""),
                NroPlantas: String(datos.NroPlantas || ""),
                DFilas: String(datos.DFilas || ""),
                DPlantas: String(datos.DPlantas || ""),
                SupPlanta: String(datos.SupPlanta || ""),
                Presupuesto: String(datos.Presupuesto || ""),
                QRFila: String(datos.QRFila || ""),
            }));

            const columnDefs = [
                { headerName: "PRODUCTOR", field: "Productor", filter: true, sortable: true, width: 180 },
                { headerName: "CHACRA", field: "Chacra", filter: true, sortable: true, width: 180 },
                { headerName: "CUADRO", field: "Cuadro", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "FILA", field: "Fila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "QR", field: "QRFila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "ESPECIE", field: "Especie", filter: true, sortable: true, width: 150 },
                { headerName: "VARIEDAD", field: "Variedad", filter: true, sortable: true, width: 150 },
                { headerName: "AÑO PLANTACIÓN", field: "AñoPlantacion", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CANT. PLANTAS", field: "NroPlantas", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                { headerName: "D. FILAS", field: "DFilas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "D. PLANTAS", field: "DPlantas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "SUP. PLANTAS", field: "SupPlanta", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "PRESUPUESTO", field: "Presupuesto", filter: true, sortable: true, width: 140, cellClass: 'cell-center' },
            ];

            const gridDiv = document.getElementById('tableDataResumen');
            if (!gridDiv) {
                return;
            }
            gridDiv.innerHTML = '';
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
                document.getElementById("class-bt-download").style.display = "block";
                document.getElementById("class-bt-upload").style.display = "block";
            } catch (alternativeError) {
                mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
            }
        } else {
            displayGeneral.style.visibility = 'hidden';
            const nota = data.Nota || "No se pudo cargar la información";
            const color = "red";
            mostrarInfo(nota, color);
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        const nota = "Se produjo un error al procesar la solicitud. " + error.message;
        const color = "red";
        mostrarInfo(nota, color);
    }
};

const enviarCenso = async () => {
    openLoading();
    try {
        const formData = new FormData();
        const archivoExcel = document.getElementById('excel-file').files[0];
        formData.append('archivoExcel', archivoExcel);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch('enviar-archivo-excel/', options);
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
                IdProductor: String(datos.IdProductor || ""),
                Productor: String(datos.Productor || ""),
                IdChacra: String(datos.IdChacra || ""),
                Chacra: String(datos.Chacra || ""),
                Cuadro: String(datos.Cuadro || ""),
                Fila: String(datos.Fila || ""),
                IdEspecie: String(datos.IdEspecie || ""),
                Especie: String(datos.Especie || ""),
                IdVariedad: String(datos.IdVariedad || ""),
                Variedad: String(datos.Variedad || ""),
                AñoPlantacion: String(datos.AñoPlantacion || ""),
                NroPlantas: String(datos.NroPlantas || ""),
                DFilas: String(datos.DFilas || ""),
                DPlantas: String(datos.DPlantas || ""),
                SupPlanta: String(datos.SupPlanta || ""),
                Presupuesto: String(datos.Presupuesto || ""),
                QRFila: String(datos.QRFila || ""),
            }));

            const columnDefs = [
                { headerName: "PRODUCTOR", field: "Productor", filter: true, sortable: true, width: 180 },
                { headerName: "CHACRA", field: "Chacra", filter: true, sortable: true, width: 180 },
                { headerName: "CUADRO", field: "Cuadro", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "FILA", field: "Fila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "QR", field: "QRFila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "ESPECIE", field: "Especie", filter: true, sortable: true, width: 150 },
                { headerName: "VARIEDAD", field: "Variedad", filter: true, sortable: true, width: 150 },
                { headerName: "AÑO PLANTACIÓN", field: "AñoPlantacion", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CANT. PLANTAS", field: "NroPlantas", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                { headerName: "D. FILAS", field: "DFilas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "D. PLANTAS", field: "DPlantas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "SUP. PLANTAS", field: "SupPlanta", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "PRESUPUESTO", field: "Presupuesto", filter: true, sortable: true, width: 140, cellClass: 'cell-center' },
            ];

            const gridDiv = document.getElementById('tableDataResumen');
            if (!gridDiv) {
                return;
            }
            gridDiv.innerHTML = '';
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
                document.getElementById("class-bt-download").style.display = "block";
                document.getElementById("class-bt-upload").style.display = "block";
            } catch (alternativeError) {
                mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
            }
            hideInnerSubirExcel();
        } else {
            var nota = data.Nota;
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






















































function getValuesProductor() {
    return choiceProductores.getValue() ? choiceProductores.getValue().value : '';
}

function getValuesChacra() {
    return choiceChacras.getValue() ? choiceChacras.getValue().value : '';
}

function getLabelChacra() {
    return choiceChacras.getValue() ? choiceChacras.getValue().label : '';
}

function changeClean() {
    displayGeneral.style.visibility = 'hidden';
    document.getElementById("class-bt-download").style.display = "none";
    document.getElementById("class-bt-upload").style.display = "none";
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

function showInnerSubirExcel(texto) {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor">
            <p>${texto}</p>
        </div>
        <div class="carga-contenedor">
            <div class="vr-fila-5">
                <div class="vr-col-btn-5">
                    <input type="text" id="file-name" placeholder="SELECCIONE ARCHIVO" readonly onclick="document.getElementById('excel-file').click();">
                    <input type="file" id="excel-file" accept=".xls" style="display: none;">
                </div>
            </div>
        </div>
        <div class="carga-contenedor">
            <div class="vr-fila-2">
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="hideInnerSubirExcel();" id="cancelar-subir-button">CANCELAR</button>
                </div>
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="enviarCenso();" id="acepta-subir-button">ACEPTAR</button>
                </div>
            </div>
        </div>
    `;
    document.getElementById("fondo-oscuro").style.display = "block";
    document.getElementById("popup-confirmacion").style.display = "block";
    document.getElementById('excel-file').addEventListener('change', function () {
        var fileName = this.files[0].name;
        document.getElementById('file-name').value = fileName;
    });
}



function hideInnerSubirExcel() {
    document.getElementById('contenido-popup').innerHTML = ``;
    document.getElementById("fondo-oscuro").style.display = "none";
    document.getElementById("popup-confirmacion").style.display = "none";
}