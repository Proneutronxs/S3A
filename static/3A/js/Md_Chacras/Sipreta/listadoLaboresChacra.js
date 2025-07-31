document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');
let jsonData;

window.addEventListener("load", async () => {
    fechaActual();
    dataInicial();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    dataDateTable();
});

document.getElementById('exportar-button').addEventListener('click', function () {
    showInnerPop();
});

desde.addEventListener("change", (event) => {
    limpiaTabla();
});

hasta.addEventListener("change", (event) => {
    limpiaTabla();
})

selector_productores.addEventListener("change", (event) => {
    limpiaTabla();
    dataSubItems();
});

selector_chacras.addEventListener("change", (event) => {
    limpiaTabla();
    dataSubItemsCuadros();
});

selector_especies.addEventListener("change", (event) => {
    limpiaTabla();
    dataSubItemsVariedades();
});

selector_cuadros.addEventListener("change", (event) => {
    limpiaTabla();
});

selector_variedades.addEventListener("change", (event) => {
    limpiaTabla();
});

const choiceProductor = new Choices('#selector_productores', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE PRODUCTOR',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceChacra = new Choices('#selector_chacras', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CHACRA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceCuadro = new Choices('#selector_cuadros', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CUADRO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEspecie = new Choices('#selector_especies', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ESPECIE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceVariedad = new Choices('#selector_variedades', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE VARIEDAD',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEncargado = new Choices('#selector_encargados', {
    allowHTML: true,
    shouldSort: false,
    //placeholderValue: 'SELECCIONE ENCARGADO',
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
                    value: datos.IdProductor, label: datos.Descripcion
                });
            });
            choiceProductor.clearChoices();
            choiceProductor.removeActiveItems();
            choiceProductor.setChoices(result, 'value', 'label', true);

            let result1 = [{ value: '', label: 'TODO' }];
            result1.push();
            data.Especies.forEach((datos) => {
                result1.push({
                    value: datos.IdEspecie, label: datos.Descripcion
                });
            });
            choiceEspecie.clearChoices();
            choiceEspecie.removeActiveItems();
            choiceEspecie.setChoices(result1, 'value', 'label', true);
        } else {
            choiceProductor.clearChoices();
            choiceProductor.removeActiveItems();
            choiceEspecie.clearChoices();
            choiceEspecie.removeActiveItems();
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

        const response = await fetch("chacra-productor/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [{ value: '', label: 'TODO' }];
            result.push();
            data.Chacras.forEach((datos) => {
                result.push({ value: datos.IdChacra, label: datos.Descripcion });
            });
            choiceChacra.clearChoices();
            choiceChacra.removeActiveItems();
            choiceChacra.setChoices(result, 'value', 'label', true);
        } else {
            choiceChacra.clearChoices();
            choiceChacra.removeActiveItems();
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const dataSubItemsVariedades = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdEspecie", getValuesEspecie());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("especie-variedad/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [{ value: '', label: 'TODO' }];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.IdVariedad, label: datos.Descripcion });
            });
            choiceVariedad.clearChoices();
            choiceVariedad.removeActiveItems();
            choiceVariedad.setChoices(result, 'value', 'label', true);
        } else {
            choiceVariedad.clearChoices();
            choiceVariedad.removeActiveItems();
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const dataSubItemsCuadros = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdChacra", getValuesChacra());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("chacra-cuadro/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [{ value: '', label: 'TODO' }];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.IdCuadro, label: datos.Descripcion });
            });
            choiceCuadro.clearChoices();
            choiceCuadro.removeActiveItems();
            choiceCuadro.setChoices(result, 'value', 'label', true);
        } else {
            choiceCuadro.clearChoices();
            choiceCuadro.removeActiveItems();
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
        formData.append("IdChacra", getValuesChacra());
        formData.append("IdCuadro", getValuesCuadro());
        formData.append("IdEspecie", getValuesEspecie());
        formData.append("IdVariedad", getValuesVariedad());

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("data-chacras/", options);
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
                Chacra: String(datos.CHACRA || ""),
                Fecha: String(datos.FECHA || ""),
                Cuadro: String(datos.CUADRO || ""),
                Fila: String(datos.FILA || ""),
                CantPlantas: String(datos.CANT_PLANTAS || ""),
                Labor: String(datos.LABOR || ""),
                ImporteFila: String(datos.IMPORTE_FILA || ""),
                Variedades: String(datos.VARIEDADES || ""),
                Presupuesto: String(datos.PRESUPUESTO || ""),
                Porcentaje: String(datos.PORCENTAJE || ""),
                Superficie: String(datos.SUPERFICIE || ""),
            }));

            const columnDefs = [
                { headerName: "CHACRA", field: "Chacra", filter: true, sortable: true, width: 180 },
                { headerName: "FECHA", field: "Fecha", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CUADRO", field: "Cuadro", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "FILA", field: "Fila", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "CANT. PLANTAS", field: "CantPlantas", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "LABOR", field: "Labor", filter: true, sortable: true, width: 100, cellClass: 'cell-center'  },
                { headerName: "VARIEDADES", field: "Variedades", filter: true, sortable: true, width: 180},
                { headerName: "IMPORTE", field: "ImporteFila", filter: true, sortable: true, width: 120, cellClass: 'cell-center' },
                { headerName: "PRESUPUESTO", field: "Presupuesto", filter: true, sortable: true, width: 120, cellClass: 'cell-center' },
                { headerName: "PORCENTAJE", field: "Porcentaje", filter: true, sortable: true, width: 100, cellClass: 'cell-center'  },
                { headerName: "SUPERFICIE", field: "Superficie", filter: true, sortable: true, width: 120, cellClass: 'cell-center' },
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
            } catch (alternativeError) {
                mostrarInfo("Error al crear la tabla: " + alternativeError.message, "red");
                closeLoading();
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

const dataDateArchivo = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdChacra", getValuesChacra());
        formData.append("IdCuadro", getValuesCuadro());
        formData.append("IdEspecie", getValuesEspecie());
        formData.append("IdVariedad", getValuesVariedad());
        formData.append("Tipo", getListadoType());
        formData.append("Filtros", JSON.stringify(getSelectedOptions()));

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("archivo-chacras/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            window.location.href = 'archivo=' + data.Archivo;
            document.getElementById("fondo-oscuro").style.display = "none";
            document.getElementById("popup-confirmacion").style.display = "none";
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

function getLabel(choices) {
    const value = choices.getValue();
    return value && value.label ? value.label : 'TODOS';
}

function getSelectedOptions() {
    return {
        PRODUCTOR: getLabel(choiceProductor),
        CHACRA: getLabel(choiceChacra),
        CUADRO: getLabel(choiceCuadro),
        ESPECIE: getLabel(choiceEspecie),
        //LABOR: getLabel(choiceLabor),
        VARIEDAD: getLabel(choiceVariedad),
        DESDE: desde.value,
        HASTA: hasta.value
    };
}





















function showInnerPop() {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor" style="border: 1px solid #ccc; margin-top: 5px; width: 380px;">
            <p>LISTADOS CHACRAS:</p>
            <div class="vr-fila-5">
                <div class="vr-col-6">
                    <div>
                        <input type="radio" id="RP" name="listado-type" value="RP">
                        <label for="RP">Res. por Chacra</label>
                    </div>
                </div>
                <div class="vr-col-6">
                    <div>
                        <input type="radio" id="DP" name="listado-type" value="DP" checked>
                        <label for="DP">Det. por Chacra</label>
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
                    <button class="vr-button" onclick="dataDateArchivo();" id="descargar-subir-button">DESCARGAR</button>
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

function getValuesProductor() {
    return choiceProductor.getValue() ? choiceProductor.getValue().value : '';
}

function getValuesChacra() {
    return choiceChacra.getValue() ? choiceChacra.getValue().value : '';
}

function getValuesCuadro() {
    return choiceCuadro.getValue() ? choiceCuadro.getValue().value : '';
}

function getValuesEspecie() {
    return choiceEspecie.getValue() ? choiceEspecie.getValue().value : '';
}

function getValuesVariedad() {
    return choiceVariedad.getValue() ? choiceVariedad.getValue().value : '';
}

function getListadoType() {
    return document.querySelector('input[name="listado-type"]:checked').value;
}

function limpiaTabla() {
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

function formatoMoneda(valor) {
    const numero = parseFloat(valor);
    const parteEntera = Math.floor(numero).toLocaleString('es-AR');
    const parteDecimal = numero.toFixed(2).split('.')[1];
    return `$ ${parteEntera},${parteDecimal}`;
}
 // style="gap: 25px;"











