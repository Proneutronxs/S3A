document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');


window.addEventListener("load", async () => {
    fechaActual();
    dataInicial();
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
});

selector_tareas.addEventListener("change", (event) => {
    displayGeneral.style.visibility = 'hidden';
});

const choiceCentro = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CENTRO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});
const choiceTarea = new Choices('#selector_tareas', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE TAREA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("lista-centros-chacras/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });

            let result2 = [];
            result2.push();
            data.Tareas.forEach((datos2) => {
                result2.push({
                    value: datos2.Codigo, label: datos2.Descripcion
                });
            });

            choiceCentro.clearChoices();
            choiceCentro.removeActiveItems();
            choiceTarea.clearChoices();
            choiceTarea.removeActiveItems();

            choiceCentro.setChoices(result, 'value', 'label', true);
            choiceTarea.setChoices(result2, 'value', 'label', true);
        } else {
            choiceCentro.clearChoices();
            choiceCentro.removeActiveItems();
            choiceTarea.clearChoices();
            choiceTarea.removeActiveItems();
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

const dataDateTable = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCentro", getValuesCentro());
        formData.append("IdLabor", getValuesLabores());
        formData.append("Tipo", "TT");
        formData.append("Filtros", JSON.stringify(getSelectedOptions()));

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("listado-labores/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {

            const rawJson = data.Datos; // Esto es tu JSON agrupado por legajo
            const jsonData = []; // Este es el que usaremos para AG Grid

            // Convertir a estructura plana
            Object.values(rawJson).forEach((legajoArray) => {
                legajoArray.forEach((registro) => {
                    const comunes = {
                        Legajo: registro.LEGAJO,
                        Nombres: registro.NOMBRES,
                        Centro: registro.CENTRO,
                        Regis: registro.REGIS,
                        Tarea: registro.TAREA
                    };

                    registro.DETALLES.forEach((detalle) => {
                        jsonData.push({
                            ...comunes,
                            Item: detalle.ITEM,
                            Cantidad: formatoDecimal(detalle.CANTIDAD),
                            Importe: formatoMoneda(detalle.IMPORTE),
                            SumaImporte: formatoMoneda(detalle.SUMA_IMPORTE)
                        });
                    });
                });
            });

            const columnDefs = [
                { headerName: "LEGAJO", field: "Legajo", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "NOMBRES", field: "Nombres", filter: true, sortable: true, width: 200 },
                { headerName: "CENTRO", field: "Centro", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                //{ headerName: "REGIS", field: "Regis", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "TAREA", field: "Tarea", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "ITEM", field: "Item", filter: true, sortable: true, width: 80, cellClass: 'cell-center' },
                { headerName: "CANTIDAD", field: "Cantidad", filter: true, sortable: true, width: 100, cellClass: 'cell-center' },
                { headerName: "IMPORTE", field: "Importe", filter: true, sortable: true, width: 120, cellClass: 'cell-center' },
                { headerName: "SUMA IMPORTE", field: "SumaImporte", filter: true, sortable: true, width: 140, cellClass: 'cell-center' }
            ];

            const gridDiv = document.getElementById('tableDataResumen');
            if (!gridDiv) {
                console.error("Div 'tableDataResumen' no encontrado.");
                closeLoading();
                return;
            }

            gridDiv.innerHTML = '';

            try {
                const gridOptions = {
                    rowHeight: 30,
                    headerHeight: 32,
                    columnDefs: columnDefs,
                    rowData: jsonData,
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

            } catch (error) {
                mostrarInfo("Error al crear la tabla: " + error.message, "red");
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

const descargar_archivo = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("IdCentro", getValuesCentro());
        formData.append("IdLabor", getValuesLabores());
        formData.append("Tipo", getListadoType());
        formData.append("Filtros", JSON.stringify(getSelectedOptions()));

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("listado-labores/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            if (data.Archivo == "e") {
                displayGeneral.style.visibility = 'hidden';
                mostrarInfo("No se pudo crear el archivo", "red");
            } else {
                window.location.href = 'archivo=' + data.Archivo;
                document.getElementById("fondo-oscuro").style.display = "none";
                document.getElementById("popup-confirmacion").style.display = "none";
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






























function getLabel(choices) {
    const value = choices.getValue();
    return value && value.label ? value.label : 'TODOS';
}

function getSelectedOptions() {
    return {
        CENTRO: getLabel(choiceCentro),
        LABOR: getLabel(choiceTarea),
        DESDE: desde.value,
        HASTA: hasta.value
    };
}

function formatoDecimal(valor) {
    const numero = parseFloat(valor);
    return numero === 0 || isNaN(numero) ? "" : numero.toFixed(2);
}

function formatoMoneda(valor) {
    const numero = parseFloat(valor);
    return isNaN(numero) ? "" : `$ ${numero.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function getListadoType() {
    return document.querySelector('input[name="listado-type"]:checked').value;
}

function getValuesCentro() {
    return choiceCentro.getValue() ? choiceCentro.getValue().value : '';
}

function getValuesLabores() {
    return choiceTarea.getValue() ? choiceTarea.getValue().value : '';
}

function showPopDescarga() {
    document.getElementById('contenido-popup').innerHTML = `
        <div class="carga-contenedor" style="border: 1px solid #ccc; margin-top: 5px; width: 350px;">
            <p>Listados Excel:</p>
            <div class="vr-fila-5">
                <div class="vr-col-6">
                    <div>
                        <input type="radio" id="RP" name="listado-type" value="RP" checked>
                        <label for="RP">Planilla Labores</label>
                    </div>
                </div>
                <div class="vr-col-6">
                    <div>
                        <input type="radio" id="AI" name="listado-type" value="AI">
                        <label for="AI">Archivo ISIS</label>
                    </div>
                </div>
            </div>
        </div>
        <div class="carga-contenedor" style="text-align: center; margin-top: 10px;">
            <div class="vr-fila-2">
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="hiddenInnerPop();" id="cancelar-descarga-button">CANCELAR</button>
                </div>
                <div class="vr-col-btn">
                    <button class="vr-button" onclick="descargar_archivo();" id="descargar-subir-button">DESCARGAR</button>
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

// `
//             <div class="vr-fila-5" style="border: 1px solid #ccc; margin-top: 5px;">
//                 <div class="vr-col-btn-5" style="text-align: center; padding: 5px;">
//                 <input type="checkbox" id="asis" name="include" value="asis" checked>
//                 <label for="asis">Incluir Asistencia</label>
//             </div>`













