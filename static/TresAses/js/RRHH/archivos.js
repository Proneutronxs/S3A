const desde = document.getElementById('fechaInicio');

const hasta = document.getElementById('fechaFinal');


window.addEventListener("load", async () => {
    fechaActual();
    verHorasArchivo();
});

selector_legajos.addEventListener("change", (event) => {
    verHorasArchivo();
});

fechaInicio.addEventListener("change", (event) => {
    verHorasArchivo();
});

fechaFinal.addEventListener("change", (event) => {
    verHorasArchivo();
});

document.getElementById('idBuscaHoras').addEventListener('click', function () {
    verHorasArchivo();
});

document.getElementById('cerrar_excel').addEventListener('click', function () {
    pop_descarga_excel.style.display = "none";
});

document.getElementById('creaExcel').addEventListener('click', function () {
    pop_descarga_excel.style.display = "flex";
});

document.getElementById('descargar_excel').addEventListener('click', function () {
    retornaExcel();
});

const choiceLegajos = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
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
    desde.value = formattedDateDesde
    hasta.value = formattedDate;
}




const verHorasArchivo = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        const Legajo = document.getElementById("selector_legajos").value;
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Legajo", Legajo);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("ver/listado-horas/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let datos_he = ``;
            data.Horas.forEach((datos) => {
                datos_he += `
                            <tr>
                                <td class="table_center">${datos.Legajo}</td>
                                <td>${datos.Nombre}</td>
                                <td class="table_center">${datos.Abrev}</td>
                                <td class="table_center">${datos.Horas50}</td>
                                <td class="table_center">${datos.Horas100}</td>
                                <td class="table_center">${datos.HorasS}</td>
                                <td class="table_center">${datos.AC50}</td>
                                <td class="table_center">${datos.AC100}</td>
                                <td>${datos.Sindicato}</td>
                            </tr>
                            `
            });
            document.getElementById('tabla_horas_totales').innerHTML = datos_he;
            let result = [];
            data.Legajos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choiceLegajos.clearChoices();
            choiceLegajos.setChoices(result, 'value', 'label', true);
            document.getElementById('contenido_popup').innerHTML = `<p>${data.Text}</p>`;
            closeProgressBar();
        } else {
            document.getElementById('tabla_horas_totales').innerHTML = ``;
            document.getElementById('contenido_popup').innerHTML = `<p>${data.Text}</p>`;
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
};


const retornaExcel = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("Indicador", '0');
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("descarga-excel-he/", options);
        const contentType = response.headers.get('content-type');
        closeProgressBar();
        pop_descarga_excel.style.display = "none";
        if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            const blob = await response.blob();
            const excelURL = URL.createObjectURL(blob);
            window.open(excelURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};



















const modalOverlay = document.querySelector('.modal-overlay');
function openProgressBar() {
    modalOverlay.style.display = 'block';
}
function closeProgressBar() {
    modalOverlay.style.display = 'none';
}
document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popup").classList.remove("active");
});

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