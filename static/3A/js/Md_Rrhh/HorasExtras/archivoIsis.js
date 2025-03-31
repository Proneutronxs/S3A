document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    dataDateTable();
});

const dataDateTable = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
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
                    columnDefs: columnDefs,
                    rowData: tableData,
                    floatingFilter: true,
                    quickFilterText: '',
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
