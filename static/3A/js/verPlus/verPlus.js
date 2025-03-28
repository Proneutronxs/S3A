const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const mercado = document.getElementById("selector_mercado");
const cliente = document.getElementById("selector_cliente");
const especie = document.getElementById("selector_especie");
const variedad = document.getElementById("selector_variedad");
const envase = document.getElementById("selector_envase");
const marca = document.getElementById("selector_marca");
const calibres = document.getElementById("selector_calibres");
const loadingContainer = document.getElementById('loading-container');




window.addEventListener("load", async () => {
    listarDataInicial();
    fechaActual();
});

selector_mercado.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
    const IdElemento = document.getElementById("selector_mercado").value;
    dataSubItems('CLI', IdElemento, 'SELECCIONE CLIENTE');
});

selector_cliente.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
});

selector_especie.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
    const IdElemento = document.getElementById("selector_especie").value;
    dataSubItems('VAR', IdElemento, 'SELECCIONE VARIEDAD');
});

selector_variedad.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
});

selector_envase.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
});

selector_marca.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
});

selector_calibres.addEventListener("change", (event) => {
    document.getElementById('id-contenedor-empresas').innerHTML = ``;
    document.getElementById('id-vr-datos-totales').innerHTML = ``;
});


document.getElementById('busqueda-button').addEventListener('click', function () {
    if (!choiceMercado.getValue()) {
        mostrarInfo("Por favor, seleccione un tipo de Mercado.", "red");
    } else {
        buscarCRC();
    }
});


const choiceMercado = new Choices('#selector_mercado', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE MERCADO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});



const choiceCliente = new Choices('#selector_cliente', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CLIENTE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEspecie = new Choices('#selector_especie', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ESPECIE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEnvase = new Choices('#selector_envase', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ENVASE',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceCalibre = new Choices('#selector_calibres', {
    allowHTML: true,
    shouldSort: false,
    removeItemButton: true,
    itemSelectText: '',
    maxItemCount: 4,
    placeholderValue: 'SELECCIONE CALIBRES',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceVariedad = new Choices('#selector_variedad', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE VARIEDAD',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceMarca = new Choices('#selector_marca', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE MARCA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const listarDataInicial = async () => {
    try {
        const response = await fetch("data-inicial/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.DataMercado.forEach((datos) => {
                result.push({ value: datos.IdMercado, label: datos.Descripcion });
            });
            choiceMercado.setChoices(result, 'value', 'label', true);

            let result1 = [];
            result1.push();
            data.DataEspecie.forEach((datos) => {
                result1.push({ value: datos.IdEspecie, label: datos.Descripcion });
            });
            choiceEspecie.setChoices(result1, 'value', 'label', true);

            let result2 = [];
            result2.push();
            data.DataEtiqueta.forEach((datos) => {
                result2.push({ value: datos.IdEtiqueta, label: datos.Descripcion });
            });
            choiceMarca.setChoices(result2, 'value', 'label', true);

            let result3 = [];
            result3.push();
            data.DataCalibres.forEach((datos) => {
                result3.push({ value: datos.IdCalibre, label: datos.Calibre });
            });
            choiceCalibre.setChoices(result3, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const dataSubItems = async (Tipo, IdElemento) => {
    try {
        const formData = new FormData();

        formData.append("Tipo", Tipo);
        formData.append("IdElemento", IdElemento);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("data-especifica/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            if (Tipo == 'VAR') {
                let result = [];
                result.push();
                data.DataListado.forEach((datos) => {
                    result.push({ value: datos.Id, label: datos.Descripcion });
                });
                choiceVariedad.clearChoices();
                choiceVariedad.removeActiveItems();
                choiceVariedad.setChoices(result, 'value', 'label', true);

                let result2 = [];
                result.push();
                data.DataListado2.forEach((datos) => {
                    result2.push({ value: datos.Id, label: datos.Descripcion });
                });
                choiceEnvase.clearChoices();
                choiceEnvase.removeActiveItems();
                choiceEnvase.setChoices(result2, 'value', 'label', true);
            }
            if (Tipo == 'CLI') {
                let result = [];
                result.push();
                data.DataListado.forEach((datos) => {
                    result.push({ value: datos.Id, label: datos.Descripcion });
                });
                choiceCliente.clearChoices();
                choiceCliente.removeActiveItems();
                choiceCliente.setChoices(result, 'value', 'label', true);
            }
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const buscarCRC = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Mercado", mercado.value);
        formData.append("Cliente", getValueCliente());
        formData.append("Especie", getValueEspecie());
        formData.append("Variedad", getValueVariedad());
        formData.append("Envase", getValueEnvase());
        formData.append("Marca", getValueMarca());
        formData.append("Calibres", getValueCalibres());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("data-busqueda/", options);
        const data = await response.json();
        document.getElementById('id-contenedor-empresas').innerHTML = ``;
        document.getElementById('id-vr-datos-totales').innerHTML = ``;
        closeLoading();
        if (data.Message == "Success") {
            data.Empresas.forEach((empresa) => {
                const encabezadoEmpresa = `
                    <div class="vr-tb-header-container">
                        <div class="vr-tb-header-main">
                            ${empresa.Nombre}
                        </div>
                        <div class="vr-tb-summary">
                            Cant. Bultos: ${empresa.Subtotal.Bultos} - SubCRC: ${empresa.Subtotal.SumaImporteCRCTotal} - SubTotal: ${empresa.Subtotal.SumaImporteTotal} - Total: ${empresa.Subtotal.TotalGeneral}
                        </div>
                    </div>
                `;
                document.getElementById('id-contenedor-empresas').innerHTML += encabezadoEmpresa;
                const tablaEmpresa = `
                    <table class="vr-tb-table">
                        <thead>
                            <tr>
                                <th class="vr-tb-header">FECHA</th>
                                <th class="vr-tb-header">ESPECIE</th>
                                <th class="vr-tb-header">VARIEDAD</th>
                                <th class="vr-tb-header">ENVASE</th>
                                <th class="vr-tb-header">MARCA</th>
                                <th class="vr-tb-header">CALIBRE</th>
                                <th class="vr-tb-header">BULTOS</th>
                                <th class="vr-tb-header">IMP. UNI.</th>
                                <th class="vr-tb-header">IMP. CRC</th>
                                <th class="vr-tb-header">IMP. TOTAL</th>
                            </tr>
                        </thead>
                        <tbody id="id-tbody-${empresa.Nombre}">
                        </tbody>
                    </table>
                `;
                document.getElementById('id-contenedor-empresas').innerHTML += tablaEmpresa;
                empresa.Datos.forEach((dato) => {
                    const filaTabla = `
                        <tr>
                            <td>${dato.FechaFac}</td>
                            <td>${dato.Especie}</td>
                            <td>${dato.Variedad}</td>
                            <td>${dato.Envase}</td>
                            <td>${dato.Marca}</td>
                            <td>${dato.Calibre}</td>
                            <td>${dato.Cantidad}</td>
                            <td>${formatoMonedaTexto(dato.Moneda,dato.ImporteUnitario)}</td>
                            <td>${formatoMonedaTexto(dato.Moneda,(multiplicar(dato.CRC, dato.Cantidad)).toString())}</td>
                            <td>${formatoMonedaTexto(dato.Moneda,(multiplicar(dato.Cantidad, dato.ImporteUnitario)).toString())}</td>
                        </tr>
                    `;
                    document.getElementById(`id-tbody-${empresa.Nombre}`).innerHTML += filaTabla;
                });
            });


            let datosTotales = `
                <div class="vr-datos-encabezado-item vr-datos-crc">
                    <strong>Cant. Total Bultos: </strong>${data.Resumen.Bultos}
                </div>
                <div class="vr-datos-encabezado-item vr-datos-crc">
                    <strong>CRC Total: </strong>${data.Resumen.SumaImporteCRCTotal}
                </div>
                <div class="vr-datos-encabezado-item vr-datos-importe">
                    <strong>Importe Total: </strong>${data.Resumen.SumaImporteTotal}
                </div>
                <div class="vr-datos-encabezado-item vr-datos-general">
                    <strong>Total General: </strong>${data.Resumen.TotalGeneral}
                </div>
            `;
            document.getElementById('id-vr-datos-totales').innerHTML = datosTotales;
        } else {
            document.getElementById('id-contenedor-empresas').innerHTML = ``;
            document.getElementById('id-vr-datos-totales').innerHTML = ``;
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
};

function getValueCliente() {
    return choiceCliente.getValue() ? choiceCliente.getValue().value : '0';
}

function getValueEspecie() {
    return choiceEspecie.getValue() ? choiceEspecie.getValue().value : '0';
}

function getValueVariedad() {
    return choiceVariedad.getValue() ? choiceVariedad.getValue().value : '0';
}

function getValueEnvase() {
    return choiceEnvase.getValue() ? choiceEnvase.getValue().value : '0';
}

function getValueMarca() {
    return choiceMarca.getValue() ? choiceMarca.getValue().value : '0';
}

function getValueCalibres() {
    const calibres = document.getElementById("selector_calibres");
    const selectedCalibres = Array.from(calibres.selectedOptions).map(option => option.value);
    if (selectedCalibres.length === 0) {
        return [0];
    }
    if (selectedCalibres.includes("0")) {
        return [0];
    }
    return selectedCalibres;
}

function formatoMonedaTexto(moneda,texto) {
    const num = parseFloat(texto.replace(/[^0-9.-]/g, ''));
    if (isNaN(num)) {
        return '-';
    }
    return moneda +` ${num.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function multiplicar(num1, num2) {
    return num1 * num2;
}

function actualizarFechaDesde(fechaHasta) {
    const fechaHastaDate = new Date(fechaHasta);
    const fechaDesdeDate = new Date(document.getElementById("vr-fecha-desde").value);

    const diferenciaMeses = diferenciaEnMeses(fechaDesdeDate, fechaHastaDate);

    if (diferenciaMeses > 3) {
        const nuevaFecha = new Date(fechaHastaDate.getFullYear(), fechaHastaDate.getMonth() - 3, fechaHastaDate.getDate());

        const dia = nuevaFecha.getDate();
        const mes = nuevaFecha.getMonth() + 1;
        const anio = nuevaFecha.getFullYear();

        const fechaDesde = `${anio}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;

        document.getElementById("vr-fecha-desde").value = fechaDesde;
    } else {
        // No hacer nada 
    }
}

function actualizarFechaHasta(fechaDesde) {
    const fechaDesdeDate = new Date(fechaDesde);
    const fechaHastaDate = new Date(document.getElementById("vr-fecha-hasta").value);

    const diferenciaMeses = diferenciaEnMeses(fechaDesdeDate, fechaHastaDate);

    if (diferenciaMeses > 3) {
        const nuevaFecha = new Date(fechaDesdeDate.getFullYear(), fechaDesdeDate.getMonth() + 3, fechaDesdeDate.getDate());

        const dia = nuevaFecha.getDate();
        const mes = nuevaFecha.getMonth() + 1;
        const anio = nuevaFecha.getFullYear();

        const fechaHasta = `${anio}-${mes.toString().padStart(2, '0')}-${dia.toString().padStart(2, '0')}`;

        document.getElementById("vr-fecha-hasta").value = fechaHasta;
    } else {
        // No hacer nada 
    }
}

function diferenciaEnMeses(fecha1, fecha2) {
    const meses = Math.abs((fecha2.getFullYear() - fecha1.getFullYear()) * 12 + fecha2.getMonth() - fecha1.getMonth());
    return meses;
}

document.getElementById("vr-fecha-desde").addEventListener("change", function () {
    const fechaDesde = document.getElementById("vr-fecha-desde").value;
    actualizarFechaHasta(fechaDesde);
});

document.getElementById("vr-fecha-hasta").addEventListener("change", function () {
    const fechaHasta = document.getElementById("vr-fecha-hasta").value;
    actualizarFechaDesde(fechaHasta);
});

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
