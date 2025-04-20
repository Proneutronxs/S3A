document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    changeClean();
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    dataDateTable();
});

document.getElementById('class-bt-download').addEventListener('click', function () {
    descargarArchivo();
});

document.getElementById('guardar-button').addEventListener('click', function () {
    envia_horas('G');
});

document.getElementById('eliminar-button').addEventListener('click', function () {
    envia_horas('E');
});

selector_estado.addEventListener("change", (event) => {
    changeClean();
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

const choiceEstado = new Choices('#selector_estado', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ESTADO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceTipoHora = new Choices('#selector_tipo', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE TIPO HORA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataDateTable = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Estado", getValueEstado());
        formData.append("Tipo", getValueTipo());
        formData.append("Archivo", 'N');

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("listar-horas-extras/", options);
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
                IDHEP: String(datos.IDhep || ""),
                Tipo: String(datos.Tipo || ""),
                Legajo: String(datos.Legajo || ""),
                Nombre: String(datos.Nombre || ""),
                Centro: String(datos.Centro || ""),
                Desde: String(datos.Desde || ""),
                Hasta: String(datos.Hasta || ""),
                Motivo: String(datos.Motivo || ""),
                Descripcion: String(datos.Descripcion || ""),
                Cantidad: String(datos.Cantidad || ""),
                Solicita: String(datos.Solicita || ""),
                Importe: String(datos.Importe || ""),
                Estado: String(datos.Estado || ""),
            }));

            const columnDefs = [
                {
                    headerName: "ID",
                    checkboxSelection: true,
                    headerCheckboxSelection: true,
                    headerCheckboxSelectionFilteredOnly: true,
                    width: 80,
                    filter: false,
                    sortable: false,
                    suppressSizeToFit: true,
                    cellClass: 'cell-center',
                    valueGetter: function (params) {
                        return params.data.IDHEP;
                    }
                },
                { headerName: "TIPO", field: "Tipo", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "LEGAJO", field: "Legajo", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "APELLIDO Y NOMBRE", field: "Nombre", filter: true, sortable: true, width: 220, cellClass: 'cell-left' },
                { headerName: "CENTRO DE COSTO", field: "Centro", filter: true, sortable: true, width: 200, cellClass: 'cell-left' },
                { headerName: "DESDE", field: "Desde", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                { headerName: "HASTA", field: "Hasta", filter: true, sortable: true, width: 150, cellClass: 'cell-center' },
                { headerName: "MOTIVO", field: "Motivo", filter: true, sortable: true, width: 150, cellClass: 'cell-left' },
                { headerName: "DESCRIPCION", field: "Descripcion", filter: true, sortable: true, width: 240, cellClass: 'cell-left' },
                { headerName: "CANTIDAD HS", field: "Cantidad", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "SOLICITA", field: "Solicita", filter: true, sortable: true, width: 180, cellClass: 'cell-left' },
                { headerName: "IMPORTE", field: "Importe", filter: true, sortable: true, width: 120, cellClass: 'cell-right' },
                { headerName: "ESTADO", field: "Estado", filter: true, sortable: true, width: 80, cellClass: 'cell-center' }
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
                    rowSelection: 'multiple',
                    suppressRowClickSelection: false,
                    isRowSelectable: function (params) {
                        return params.data.Estado !== 'A';
                    },
                    getRowClass: function (params) {
                        if (params.data.Estado === 'A') {
                            return 'disabled-row';
                        }
                    },
                    defaultColDef: {
                        resizable: true 
                    },
                    onGridReady: function(params) {
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

const descargarArchivo = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Estado", getValueEstado());
        formData.append("Tipo", getValueTipo());
        formData.append("Archivo", 'S');

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch('listar-horas-extras/', options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else {
            window.location.href = 'archivo=' + data.Archivo;
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const envia_horas = async (metodo) => {
    openLoading();
    try {
        if (typeof gridOptions === 'undefined' || !gridOptions || !gridOptions.api) {
            mostrarInfo("No se buscaron horas.", "red");
            closeLoading();
            return;
        }
        const selectedRows = gridOptions.api.getSelectedRows();
        if (selectedRows.length === 0) {
            mostrarInfo("Por favor, seleccione al menos una fila", "orange");
            closeLoading();
            return;
        }
        const formData = new FormData();
        formData.append("Importe", getValueArreglo());
        formData.append("Metodo", metodo);
        selectedRows.forEach((row, index) => {
            formData.append(`IDhep${index}`, row.IDHEP);
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

function changeClean() {
    document.getElementById("class-bt-download").style.display = "none";
    displayGeneral.style.visibility = 'hidden';
}

function getValueArreglo() {
    return document.getElementById('valor-arreglo').value.replace(/\./g, '') || '';
}

function getValueEstado() {
    return choiceEstado.getValue() ? choiceEstado.getValue().value : '1';
}

function getValueTipo() {
    return choiceTipoHora.getValue() ? choiceTipoHora.getValue().value : '';
}

document.getElementById('valor-arreglo').addEventListener('input', function () {
    let valor = this.value.replace(/\./g, '');
    valor = parseInt(valor);
    if (isNaN(valor) || valor < 0 || valor % 100 !== 0) {
        this.style.border = '1px solid red';
    } else {
        this.style.border = '';
    }
    this.value = valor.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
});

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
