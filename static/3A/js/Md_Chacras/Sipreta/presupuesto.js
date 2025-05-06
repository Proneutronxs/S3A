document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const busquedaChacras = document.getElementById('busqueda-chacras');
const confirmacionChacras = document.getElementById('confirmacion-chacras');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');
let jsonData;
let valor;

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
    if (!choiceProductores.getValue() || !choiceChacras.getValue()) {
        mostrarInfo("Por favor, seleccione un Productor y Chacra.", "red");
    } else {
        dataDateTable();
    }
});

document.getElementById('class-bt-download').addEventListener('click', function () {
    if (!choiceProductores.getValue() || !choiceChacras.getValue()) {
        mostrarInfo("Por favor, seleccione un Productor y Chacra.", "red");
    } else {
        descargaExcel();
    }
});

document.getElementById('class-bt-upload').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    busquedaChacras.style.display = 'none';
    showInnerSubirExcel('SUBIR ALTA CHACRA');
});

document.getElementById('class-bt-pres').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    busquedaChacras.style.display = 'none';
    subirPresupuesto('SUBIR PRESUPUESTO');
});

document.getElementById('cancelar-up').addEventListener('click', function () {
    confirmacionChacras.style.display = 'none';
    busquedaChacras.style.display = 'block';
    displayGeneral.style.visibility = 'hidden';
});

document.getElementById('confirmar-up').addEventListener('click', function () {
    if (valor == 'C'){
        insertarCenso();
    } 
    if (valor == 'P'){
        insertarPresupuesto();
    } 
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
                closeLoading();
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
            closeLoading();
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

const descargaExcel = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdProductor", getValuesProductor());
        formData.append("IdChacra", getValuesChacra());
        formData.append("Tipo", "TB");

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("data-listado/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            window.location.href = 'archivo='+data.Excel;            
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

        const options = { method: 'POST', body: formData };
        const response = await fetch('enviar-archivo-excel/', options);
        const data = await response.json();

        if (data.Message === "Not Authenticated") {
            window.location.href = data.Redirect;
            return;
        }

        if (data.Message !== "Success") {
            mostrarInfo(data.Nota || "Error desconocido", "red");
            closeLoading();
            return;
        }
        jsonData = data.Datos;
        if (!jsonData || !Array.isArray(jsonData.Chacras) || jsonData.Chacras.length === 0) {
            displayGeneral.style.visibility = 'hidden';
            mostrarInfo("No se encontraron datos para mostrar", "orange");
            closeLoading();
            return;
        }
        const gridContainer = document.getElementById('tableDataResumen');
        if (!gridContainer) {
            mostrarInfo("No se encontró el contenedor de la tabla", "red");
            closeLoading();
            return;
        }
        gridContainer.innerHTML = '';

        if (typeof agGrid === 'undefined') {
            mostrarInfo("Error: La biblioteca de tabla no está disponible", "red");
            closeLoading();
            return;
        }
        jsonData.Chacras.forEach((chacra, index) => {
            const { IdCracra, Chacra, Productor, Cuadros } = chacra;
            const encabezado = document.createElement('div');
            encabezado.className = 'usuario-encabezado';
            encabezado.innerHTML = `
                <h3>
                    <span><strong></strong>${IdCracra}</span> -
                    <span><strong></strong>${Chacra}</span> -
                    <span><strong></strong>${Productor}</span>
                </h3>
            `;
            gridContainer.appendChild(encabezado);
            const tableData = [];
            Cuadros.forEach((cuadroObj) => {
                Object.keys(cuadroObj).forEach((cuadroKey) => {
                    const filas = cuadroObj[cuadroKey];
                    filas.forEach((fila) => {
                        tableData.push({
                            IdProductor: "",
                            Productor: Productor,
                            IdChacra: IdCracra,
                            Chacra: Chacra,
                            Cuadro: cuadroKey,
                            Fila: fila.Fila,
                            IdEspecie: fila.IdEspecie,
                            Especie: fila.Especie,
                            IdVariedad: fila.Idvariedad,
                            Variedad: fila.Variedad,
                            AñoPlantacion: fila.Año,
                            NroPlantas: fila.NroPlantas,
                            DFilas: fila.DistFilas,
                            DPlantas: fila.DistPlantas,
                            SupPlanta: fila.Superficie,
                            Presupuesto: fila.Presupuesto,
                            QRFila: ""
                        });
                    });
                });
            });

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

            const gridDiv = document.createElement('div');
            gridDiv.id = `grid_${IdCracra}`;
            gridDiv.style.width = '100%';
            gridDiv.style.height = 'auto';
            gridDiv.className = 'ag-theme-alpine';
            gridContainer.appendChild(gridDiv);

            const gridOptions = {
                rowHeight: 30,
                headerHeight: 32,
                headerClass: 'header-centered',
                columnDefs,
                rowData:tableData,
                domLayout: 'autoHeight',
                floatingFilter: true,
                quickFilterText: '',
                defaultColDef: {
                    resizable: true
                },
                onGridReady: function (params) {
                    params.api.sizeColumnsToFit();
                }
            };

            agGrid.createGrid(gridDiv, gridOptions);
        });
        valor = 'C';
        displayGeneral.style.visibility = 'visible';
        confirmacionChacras.style.display = 'block';
        hideInnerSubirExcel();
        closeLoading();
    } catch (error) {
        closeLoading();
        mostrarInfo("Se produjo un error al procesar la solicitud. " + error.message, "red");
    }
};

const insertarCenso = async () => {
    try {
        openLoading();
        const formData = new FormData();
        const datosPlano = prepararDatosChacras(jsonData);
        formData.append('Chacras', JSON.stringify(jsonData));
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch('insertar-chacras/', options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            displayGeneral.style.visibility = 'hidden';
            confirmacionChacras.style.display = 'none';
            busquedaChacras.style.display = 'block';
            hideInnerSubirExcel();
            mostrarInfo(data.Nota, 'green');
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

const enviarPresupuesto = async () => {
    openLoading();
    try {
        const formData = new FormData();
        const archivoExcel = document.getElementById('excel-file').files[0];
        formData.append('archivoExcel', archivoExcel);

        const options = { method: 'POST', body: formData };
        const response = await fetch('enviar-presupuesto-excel/', options);
        const data = await response.json();

        if (data.Message === "Not Authenticated") {
            window.location.href = data.Redirect;
            return;
        }
        if (data.Message !== "Success") {
            mostrarInfo(data.Nota || "Error desconocido", "red");
            closeLoading();
            return;
        }
        jsonData = data.Datos;
        if (!Array.isArray(jsonData) || jsonData.length === 0) {
            displayGeneral.style.visibility = 'hidden';
            mostrarInfo("No se encontraron datos para mostrar", "orange");
            closeLoading();
            return;
        }

        const tableData = jsonData.map((datos) => ({
            Productor: String(datos.Productor || ""),
            IdChacra: String(datos.IdChacra || ""),
            Chacra: String(datos.Chacra || ""),
            IdCuadro: String(datos.IdCuadro || ""),
            Cuadro: String(datos.Cuadro || ""),
            Fila: String(datos.Fila || ""),
            CantPlantas: String(datos.CantPlantas || ""),
            IdVariedad: String(datos.IdVariedad || ""),
            Variedad: String(datos.Variedad || ""),
            Año: String(datos.Año || ""),
            Poda: String(datos.Poda || ""),
            Raleo: String(datos.Raleo || ""),
        }));

        const columnDefs = [
            { headerName: "CHACRA", field: "Chacra", filter: true, sortable: true, width: 180 },
            { headerName: "CUADRO", field: "Cuadro", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
            { headerName: "FILA", field: "Fila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
            { headerName: "PLANTAS", field: "CantPlantas", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
            { headerName: "VARIEDAD", field: "Variedad", filter: true, sortable: true, width: 150 },
            { headerName: "AÑO", field: "Año", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
            { headerName: "PODA $", field: "Poda", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
            { headerName: "RALEO $", field: "Raleo", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
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
            valor = 'P';
            confirmacionChacras.style.display = 'block';
            displayGeneral.style.visibility = 'visible';
        } catch (alternativeError) {
            mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
        }        
        hideInnerSubirExcel();
        closeLoading();
    } catch (error) {
        closeLoading();
        mostrarInfo("Se produjo un error al procesar la solicitud. " + error.message, "red");
    }
};

const insertarPresupuesto = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append('Presupuesto', JSON.stringify(jsonData));
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch('insertar-presupuesto/', options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            displayGeneral.style.visibility = 'hidden';
            confirmacionChacras.style.display = 'none';
            busquedaChacras.style.display = 'block';
            hideInnerSubirExcel();
            mostrarInfo(data.Nota, 'green');
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

function prepararDatosChacras(jsonData) {
    const datosPlano = [];

    for (const chacra of jsonData.Chacras) {
        const { IdCracra, Chacra, Productor, Cuadros } = chacra;

        for (const cuadro of Cuadros) {
            for (const numeroCuadro in cuadro) {
                const filas = cuadro[numeroCuadro];

                for (const fila of filas) {
                    datosPlano.push({
                        IdCracra,
                        Chacra,
                        Productor,
                        Cuadro: numeroCuadro,
                        Fila: fila.Fila || "",
                        IdEspecie: parseFloat(fila.IdEspecie) || null,
                        Especie: fila.Especie || "",
                        IdVariedad: parseFloat(fila.Idvariedad) || null,
                        Variedad: fila.Variedad || "",
                        Año: parseInt(fila.Año) || null,
                        NroPlantas: parseInt(fila.NroPlantas) || 0,
                        DistFilas: parseFloat(fila.DistFilas) || 0,
                        DistPlantas: parseFloat(fila.DistPlantas) || 0,
                        Superficie: parseFloat(fila.Superficie) || 0,
                        Presupuesto: fila.Presupuesto ? parseFloat(fila.Presupuesto) : null,
                        QR: fila.QR || null
                    });
                }
            }
        }
    }

    return datosPlano;
}












































function enviarArchivoPresupuesto() {
    if (verificarArchivoExcel()) {
        enviarPresupuesto();
    } else {
        mostrarInfo('Debe seleccionar un archivo excel.', 'red')
    }
}

function enviarArchivo() {
    if (verificarArchivoExcel()) {
        enviarCenso();
    } else {
        mostrarInfo('Debe seleccionar un archivo excel.', 'red')
    }
}

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
                    <input type="text" id="file-name" placeholder="CLICK PARA BUSCAR EL ARCHIVO" readonly onclick="document.getElementById('excel-file').click();">
                    <input type="file" id="excel-file" accept=".xls, .xlsx" style="display: none;">
                </div>
            </div>
        </div>
        <div class="carga-contenedor">
            <div class="vr-fila-2">
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="cancelarSubida();" id="cancelar-subir-button">CANCELAR</button>
                </div>
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="enviarArchivo();" id="acepta-subir-button">ACEPTAR</button>
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

function subirPresupuesto(texto) {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor">
            <p>${texto}</p>
        </div>
        <div class="carga-contenedor">
            <div class="vr-fila-5">
                <div class="vr-col-btn-5">
                    <input type="text" id="file-name" placeholder="CLICK PARA BUSCAR EL ARCHIVO" readonly onclick="document.getElementById('excel-file').click();">
                    <input type="file" id="excel-file" accept=".xlsx" style="display: none;">
                </div>
            </div>
        </div>
        <div class="carga-contenedor">
            <div class="vr-fila-2">
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="cancelarSubida();" id="cancelar-subir-button">CANCELAR</button>
                </div>
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="enviarArchivoPresupuesto();" id="acepta-subir-button">ACEPTAR</button>
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

function verificarArchivoExcel() {
    const archivo = document.getElementById('excel-file').files[0];
    if (!archivo) {
        return false; 
    }
    const extensionesValidas = ['.xlsx','.xls'];
    const extension = archivo.name.substring(archivo.name.lastIndexOf('.')).toLowerCase();
    return extensionesValidas.includes(extension);
}

function cancelarSubida() {
    busquedaChacras.style.display = 'block';
    document.getElementById('contenido-popup').innerHTML = ``;
    document.getElementById("fondo-oscuro").style.display = "none";
    document.getElementById("popup-confirmacion").style.display = "none";
}

function hideInnerSubirExcel() {
    document.getElementById('contenido-popup').innerHTML = ``;
    document.getElementById("fondo-oscuro").style.display = "none";
    document.getElementById("popup-confirmacion").style.display = "none";
}