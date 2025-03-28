const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-principal');


window.addEventListener("load", async () => {
    dataInicial();
    fechaActual();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    if (!choiceEmpaques.getValue()) {
        mostrarInfo("Por favor, seleccione un Empaque.", "red");
    } else {
        sync_listados();
    }
});

selector_empaque.addEventListener("change", (event) => {
    clean_items();
});

desde.addEventListener("change", (event) => {
    clean_items();
});

hasta.addEventListener("change", (event) => {
    clean_items();
});

const choiceEmpaques = new Choices('#selector_empaque', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE EMPAQUE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("data-empaques/");
        const data = await response.json();
        closeLoading();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Empaques.forEach((datos) => {
                result.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });
            choiceEmpaques.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const sync_listados = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Incio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Empaque", getValueEmpaque());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("data-listados/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let datosProceso = ``;
            data.DatosProceso.forEach((datos) => {
                datosProceso += `
                    <tr class="pfa-tabla-fila">
                        <td class="pfa-tabla-celda text-center">${datos.Empaque}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Lote}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Productor}</td>
                        <td class="pfa-tabla-celda text-left">${datos.Variedad}</td>
                        <td class="pfa-tabla-celda text-center">${datos.Bins}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Fecha}</td>
                        <td class="pfa-tabla-celda text-right">${datos.Hora}</td>
                    </tr>
                `
            });
            document.getElementById('encabezado-proceso').innerHTML = `
                <div class="item">
                    <strong class="titulo">LOTES EN PROCESO:</strong> ${getEmpaqueSeleccionado()}
                </div>
                <div class="item">
                    <strong class="titulo">TOTAL BINS:</strong> ${data.TotalBins}
                </div>
                <div class="item">
                    <strong class="titulo">Kg PROCESADOS:</strong> ${data.TotalKilos} Kg.
                </div>
            `;

            document.getElementById('encabezado-calibres').innerHTML = `
                <div class="item">
                    <strong class="titulo">CANTIDAD DE CAJAS POR:</strong> CALIBRES
                </div>
                <div class="item">
                    <strong class="titulo">TOTAL CAJAS:</strong> ${data.TotalCajas}
                </div>
            `;

            document.getElementById('encabezado-marcas').innerHTML = `
                <div class="item">
                    <strong class="titulo">CANTIDAD DE CAJAS POR:</strong> MARCAS
                </div>
                <div class="item">
                    <strong class="titulo">TOTAL CAJAS:</strong> ${data.TotalCajas}
                </div>
            `;

            document.getElementById('encabezado-envases').innerHTML = `
                <div class="item">
                    <strong class="titulo">CANTIDAD DE CAJAS POR:</strong> ENVASES
                </div>
                <div class="item">
                    <strong class="titulo">TOTAL CAJAS:</strong> ${data.TotalCajas}
                </div>
            `;

            document.getElementById('encabezado-categorias').innerHTML = `
                <div class="item">
                    <strong class="titulo">CANTIDAD DE CAJAS POR:</strong> CATEGORÍA
                </div>
                <div class="item">
                    <strong class="titulo">TOTAL CAJAS:</strong> ${data.TotalCajas}
                </div>
            `;


            let datosCalibres = ``;
            data.DatosCalibres.forEach((datos) => {
                datosCalibres += `
                <tr class="pfa-tabla-fila">
                    <td class="pfa-tabla-celda text-center">${datos.Calibre}</td>
                    <td class="pfa-tabla-celda text-center">${datos.Cantidad}</td>
                </tr>
                `
            });

            let datosMarcas = ``;
            data.DatosMarcas.forEach((datos) => {
                datosMarcas += `
                <tr class="pfa-tabla-fila">
                    <td class="pfa-tabla-celda text-left">${datos.Marca}</td>
                    <td class="pfa-tabla-celda text-center">${datos.Cantidad}</td>
                </tr>
                `
            });

            let datosEnvases = ``;
            data.DatosEnvases.forEach((datos) => {
                datosEnvases += `
                <tr class="pfa-tabla-fila">
                    <td class="pfa-tabla-celda text-left">${datos.Envase}</td>
                    <td class="pfa-tabla-celda text-center">${datos.Cantidad}</td>
                </tr>
                `
            });

            let datosCategorias = ``;
            data.DatosCategorias.forEach((datos) => {
                datosCategorias += `
                <tr class="pfa-tabla-fila">
                    <td class="pfa-tabla-celda text-left">${datos.Categoria}</td>
                    <td class="pfa-tabla-celda text-center">${datos.Cantidad}</td>
                </tr>
                `
            });

            renderChart(data.DatosCalibres, 'bar', 'graficoCalibres');
            renderChart(data.DatosMarcas, 'pie', 'graficoMarcas');
            renderChart(data.DatosEnvases, 'pie', 'graficoEnvases');
            renderChart(data.DatosCategorias, 'pie', 'graficoCategorias');

            document.getElementById('pfa-tabla-DataLotesProceso').innerHTML = datosProceso;
            document.getElementById('pfa-tabla-DataCalibres').innerHTML = datosCalibres;
            document.getElementById('pfa-tabla-DataMarcas').innerHTML = datosMarcas;
            document.getElementById('pfa-tabla-DataEnvases').innerHTML = datosEnvases;
            document.getElementById('pfa-tabla-DataCategorias').innerHTML = datosCategorias;
            displayGeneral.style.visibility = 'visible';
        } else {
            clean_items();
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

function renderChart(data, chartType, canvasId) {
    if (!Array.isArray(data) || data.length === 0) {
        return;
    }
    const ctx = document.getElementById(canvasId).getContext('2d');
    if (window.charts && window.charts[canvasId]) {
        window.charts[canvasId].destroy();
    }
    if (!window.charts) {
        window.charts = {};
    }

    let labels = [];
    let values = [];

    if (data[0].Calibre) {
        labels = data.map(item => item.Calibre);
        values = data.map(item => parseInt(item.Cantidad));
    } else if (data[0].Marca) {
        labels = data.map(item => item.Marca);
        values = data.map(item => parseInt(item.Cantidad));
    } else if (data[0].Envase) {
        labels = data.map(item => item.Envase);
        values = data.map(item => parseInt(item.Cantidad));
    } else if (data[0].Categoria) {
        labels = data.map(item => item.Categoria);
        values = data.map(item => parseInt(item.Cantidad));
    } else {
        return;
    }
    const total = values.reduce((acc, value) => acc + value, 0);

    const isPieChart = chartType === 'pie' || chartType === 'doughnut';
    const showPercentage = isPieChart && (data[0].Marca || data[0].Envase || data[0].Categoria);

    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                display: chartType !== 'pie' && chartType !== 'doughnut' 
            }
        }
    };
    if (showPercentage) {
        chartOptions.plugins = {
            tooltip: {
                callbacks: {
                    label: function (context) {
                        const value = context.raw;
                        const percentage = ((value / total) * 100).toFixed(1);
                        return `${context.label}: ${value} (${percentage}%)`;
                    }
                }
            }
        };
    }

    window.charts[canvasId] = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: 'Cantidad',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: chartOptions
    });
}

function clean_items() {
    displayGeneral.style.visibility = 'hidden';
    document.getElementById('pfa-tabla-DataLotesProceso').innerHTML = ``;
    document.getElementById('pfa-tabla-DataCalibres').innerHTML = ``;
    document.getElementById('pfa-tabla-DataMarcas').innerHTML = ``;
    document.getElementById('pfa-tabla-DataEnvases').innerHTML = ``;
    document.getElementById('encabezado-proceso').innerHTML = ``;
    document.getElementById('encabezado-marcas').innerHTML = ``;
    document.getElementById('encabezado-calibres').innerHTML = ``;
    document.getElementById('encabezado-envases').innerHTML = ``;
}

function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    desde.value = formattedDate;
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

function getValueEmpaque() {
    return choiceEmpaques.getValue() ? choiceEmpaques.getValue().value : '0';
}

const getEmpaqueSeleccionado = () => {
    const value = choiceEmpaques.getValue(true);
    const option = document.querySelector(`#selector_empaque option[value="${value}"]`);
    return option.textContent;
}