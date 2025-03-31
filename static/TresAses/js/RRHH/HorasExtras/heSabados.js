
const timeInput50 = document.getElementById('timeInput50');
const timeInput100 = document.getElementById('timeInput100');
const formattedTime = document.getElementById('formattedTime');
const confirmaEnviar = document.getElementById('pop-agrega');
const timePattern = /^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$/;
const excelFileInput = document.getElementById('excelFile');



window.addEventListener("load", async () => {
    dataInicial();

});


selector_sabados.addEventListener("change", (event) => {
    dataDateTable();
});

document.getElementById('idActualizaHoras').addEventListener('click', function () {
    if (getValueSabados() == '') {
        mostrarInfo('Debe seleccionar un día.', 'red');
    } else {
        dataDateTable();
    }
});

document.getElementById('idDescargaExcel').addEventListener('click', function () {
    window.location.href = 'Archivo_Horas_Sabados.xlsx';
});

document.getElementById('idSubeExcel').addEventListener('click', function () {
    confirmaEnviar.style.display = 'block';
});


const choiceSabados = new Choices('#selector_sabados', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE UN DIA SÁBADO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openProgressBar();
    try {
        const response = await fetch("listar-sabados/");
        const data = await response.json();
        closeProgressBar();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({
                    value: datos.IdValue, label: datos.Value
                });
            });
            choiceSabados.clearChoices();
            choiceSabados.removeActiveItems();
            choiceSabados.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const dataDateTable = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("IdFecha", getValueSabados())
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-tabla/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let datosTabla = ``;
            data.Datos.forEach((datos) => {
                datosTabla += `
                     <div class="cardHora">
                        <div class="leftDiv">
                            <div class="horas-item">
                                <input class="input-checkbox-hs checkbox" type="checkbox" style="display: none;" id="idCheck" name="idCheck"
                                    value="${datos.Legajo}">
                                <strong>${datos.Legajo} - ${datos.Nombre}</strong>
                            </div>
                            <div class="horas-item">
                                <strong>FICHADAS: </strong>${(datos.Fichadas).toString().replace(/,/g, '  -  ')}
                            </div>
                        </div>
                        <div class="rightDiv">
                            <div class="horas-item">
                                <strong>${datos.Dia}</strong>
                            </div>
                             <!-- <div class="horas-item">
                                <label class="letras" for="cantHoras">50% :</label>
                                <input class="time-input50" type="text" id="timeInput50" name="time" placeholder="HH:mm">
                                <label class="letras" for="cantHoras">100% :</label>
                                <input class="time-input100" type="text" id="timeInput100" name="time" placeholder="HH:mm">
                            </div>
                            <p id="formattedTime" class="error-message" style="color: red; font-weight: bold;"></p> -->
                        </div>
                    </div>
                `
            });


            document.getElementById('horas_sabados').innerHTML = datosTabla;
            document.getElementById('idDescargaExcel').style.display = 'block';
            document.getElementById('idSubeExcel').style.display = 'block';
        } else {
            document.getElementById('horas_sabados').innerHTML = ``;
            document.getElementById('idDescargaExcel').style.display = 'none';
            document.getElementById('idSubeExcel').style.display = 'none';
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        document.getElementById('idDescargaExcel').style.display = 'none';
        document.getElementById('idSubeExcel').style.display = 'none';
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const enviarArchivoExcel = async () => {
    confirmaEnviar.style.display = 'none';
    openProgressBar();

    try {
        const formData = new FormData();
        const archivoExcel = document.getElementById('excelFile').files[0];
        formData.append('archivoExcel', archivoExcel);
        formData.append("IdFecha", getValueSabados())
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch('enviar-archivo-excel/', options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            dataInicial();
            document.getElementById('horas_sabados').innerHTML = ``;
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
        } else {
            dataInicial();
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

const enviarDatosTabla = async () => {
    confirmaEnviar.style.display = 'none';
    openProgressBar();
    try {
        const formData = new FormData();
        const filas = document.querySelectorAll('.cardHora');
        filas.forEach(row => {
            const legajo = row.querySelector('input[type="checkbox"]').value;
            const timeInput50 = row.querySelector('.time-input50').value;
            const timeInput100 = row.querySelector('.time-input100').value;
            formData.append('Legajo[]', legajo);
            formData.append('timeInput50[]', timeInput50);
            formData.append('timeInput100[]', timeInput100);
        });
        formData.append("IdFecha", getValueSabados())
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch('enviar-tabla/', options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            document.getElementById('horas_sabados').innerHTML = ``;
            dataInicial();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota, color);
        } else {
            var nota = data.Nota
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

document.getElementById('horas_sabados').addEventListener('input', (event) => {
    if (event.target.classList.contains('time-input50') ||
        event.target.classList.contains('time-input100')) {
        let valor = event.target.value;
        valor = valor.replace(/[^\d]/g, '');
        if (valor.length >= 2) {
            valor = valor.slice(0, 2) + ':' + valor.slice(2, 4);
        }
        if (valor.length > 5) {
            valor = valor.slice(0, 5);
        }
        event.target.value = valor;
        validarHora(event.target);
    }
});

const validarHora = (input) => {
    const valor = input.value;
    const regex = /^([01][0-9]|2[0-3]):[0-5][0-9]$/;
    const formattedTimeElement = input.closest('.rightDiv').querySelector('#formattedTime');

    if (valor.length === 5 && !regex.test(valor)) {
        formattedTimeElement.textContent = 'Hora no válida. Use formato 00:00 a 23:59';
        input.classList.add('error');
    } else {
        formattedTimeElement.textContent = '';
        input.classList.remove('error');
    }
};

function getValueSabados() {
    return choiceSabados.getValue() ? choiceSabados.getValue().value : '';
}

function cancelaEnvío() {
    confirmaEnviar.style.display = 'none';
}

function preguntaEnvío() {
    const horasSabados = document.getElementById('horas_sabados');
    if (horasSabados.children.length > 0) {
        confirmaEnviar.style.display = 'block';
    } else {
        mostrarInfo("Debe buscar y completar al menos un item.", "red");
    }
}

excelFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const fileType = file.type;

    if (fileType !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' && fileType !== 'application/vnd.ms-excel') {
        alert('Por favor, seleccione un archivo Excel válido (.xlsx o .xls)');
        excelFileInput.value = '';
    }
});






























































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