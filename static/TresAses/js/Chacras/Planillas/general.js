

const desde = document.getElementById('fechaInicio');
//const expoDesde = document.getElementById('exporta-planilla-fecha-desde');
const hasta = document.getElementById('fechaFinal');
//const expoHasta = document.getElementById('exporta-planilla-fecha-hasta');
const selectAllCheckbox = document.getElementById('selectAll');
const openPopupBtn = document.getElementById('open-popup');
const popup = document.getElementById('pop_up_detalles');
const closePopupBtn = document.getElementById('close-popup');
const exportaPopup = document.getElementById('exporta-planilla-popup');
const exportaCloseBtn = exportaPopup.querySelector('.exporta-planilla-close-popup');
const popUpPremio = document.getElementById('confirmationPopupPremio');

window.addEventListener("load", async () => {
    fechaActual();
    listarCentros();
    popUpPremio.style.display = "none";
});

selector_centros.addEventListener("change", (event) => {
    choiceLegajos.removeActiveItems();
    listarPersonalCentro();
    limpiar();
});

selector_legajos.addEventListener("change", (event) => {
    limpiar();
});

selector_descripcion.addEventListener("change", (event) => {
    limpiar();
});

selector_pagos.addEventListener("change", (event) => {
    limpiar();
});

document.getElementById('idBuscaAdicional').addEventListener('click', function () {
    completarTablaA();
});

document.getElementById('addPremio').addEventListener('click', function () {
    popUpPremio.style.display = "flex";
});

document.getElementById('cancelar_Premio').addEventListener('click', function () {
    console.log("HOLA")
    popUpPremio.style.display = "none";
});

document.getElementById('cancelar_id').addEventListener('click', function () {
    confirmacion_id.style.display = "none";
});

document.getElementById('idEliminar').addEventListener('click', function () {
    var tabla = document.getElementById('tabla_adicionales');
    var checkboxes = tabla.querySelectorAll('input[type="checkbox"]');
    var mostrarError = true;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            confirmacion_id.style.display = "flex";
            mostrarError = false;
        }
    });
    if (mostrarError) {
        var nota = "Debe seleccionar un Item.";
        var color = "red";
        mostrarInfo(nota, color);
    }
});

const choiceLegajos = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choicePagos = new Choices('#selector_pagos', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceDescripcion = new Choices('#selector_descripcion', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const listarCentros = async () => {
    try {
        const response = await fetch("listar-centros/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Codigo, label: datos.Descripcion });
            });
            choiceCentros.setChoices(result, 'value', 'label', true);
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

const listarPersonalCentro = async () => {
    try {
        const formData = new FormData();
        const centro = document.getElementById("selector_centros").value;
        formData.append("Centro", centro);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-personal/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let result = [{ value: '0', label: 'SELECCIONE UN LEGAJO', disabled: true, selected: true }];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choiceLegajos.clearChoices();
            choiceLegajos.setChoices(result, 'value', 'label', true);
        } else {
            choiceLegajos.clearChoices();
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
    // expoDesde.value = formattedDateDesde;
    // expoHasta.value = formattedDate;
}

const completarTablaA = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        const Centro = document.getElementById("selector_centros").value;
        const Legajo = document.getElementById("selector_legajos").value;
        const Descripcion = document.getElementById("selector_descripcion").value;
        const Pago = document.getElementById("selector_pagos").value;
        formData.append("Inicio", desde.value);
        formData.append("Final", hasta.value);
        formData.append("Legajo", Legajo);
        formData.append("Centro", Centro);
        formData.append("Descripcion", Descripcion);
        formData.append("Pago", Pago);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-adicionales/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            selectAllCheckbox.checked = false;
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `
                            <tr>
                                <td class="texto-centro">
                                    <input class="input-checkbox checkbox" type="checkbox" name="idCheck"
                                        value="${datos.Id}">
                                </td>
                                <td class="texto-centro" style="background-color: ${datos.Estado}; padding: 2px;"></td>
                                <td class="texto-centro">${datos.Legajo}</td>
                                <td>${datos.Nombre}</td>
                                <td class="texto-centro">${datos.Centro}</td>
                                <td class="texto-centro">${datos.Descripcion}</td>
                                <td class="texto-centro">${datos.Tarea}</td>
                                <td class="texto-centro">${datos.Dias}</td>
                                <td class="texto-centro">${datos.Cantidad}</td>
                                <td class="texto-centro">${datos.Tipo}</td>
                                <td class="texto-centro">${datos.Chacra}</td>
                                <td class="texto-centro"><input class="input" style="width: 90px; text-align: end;" type="number" value="${datos.ImportePremio}" ${datos.Epremio === 'N' ? 'disabled' : ''}></td>
                                <td class="texto-centro">${datos.Pago}</td>
                                <td class="texto-centro"><input class="input" style=" max-width: 90px; text-align: end;" type="number" value="${datos.Importe}"  ${datos.Eimporte === 'N' ? 'disabled' : ''}></td>
                                <td class="texto-centro">
                                    <button class="boton-detalles" onclick="masDetalles(${datos.Id});">
                                        <i class='bx material-symbols-outlined icon'>description</i>
                                    </button>
                                </td>
                            </tr>
                            `
            });
            document.getElementById('tabla_adicionales').innerHTML = datos_he;

            const checkboxes = document.getElementsByName('idCheck');
            selectAllCheckbox.addEventListener("change", function () {
                checkboxes.forEach(checkbox => {
                    checkbox.checked = selectAllCheckbox.checked;
                });
            });
            const individualCheckboxes = document.querySelectorAll(".input-checkbox");
            individualCheckboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {
                    if (!checkbox.checked) {
                        selectAllCheckbox.checked = false;
                    } else {
                        const allChecked = Array.from(individualCheckboxes).every(checkbox => checkbox.checked);
                        selectAllCheckbox.checked = allChecked;
                    }
                });
            });
            closeProgressBar();
        } else {
            limpiar();
            closeProgressBar();
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

const elimina_adicionales = async () => {
    openProgressBar();
    try {
        
        const checkboxes = document.querySelectorAll('.input-checkbox:checked');
        const formData = new FormData();

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('idCheck', checkbox.value);
            }
        });

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("eliminar-adicionales/", options);
        const data = await response.json();
        confirmacion_id.style.display = "none";
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            completarTablaA();       
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        confirmacion_id.style.display = "none";
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota,color);
    }
};





// Función para abrir el pop-up
function openExportaPopup() {
    exportaPopup.style.display = 'flex';
}

// Cerrar pop-up
exportaCloseBtn.addEventListener('click', () => {
    exportaPopup.style.display = 'none';
});

// Cerrar pop-up al hacer clic fuera del contenido
// window.addEventListener('click', (e) => {
//     if (e.target === exportaPopup) {
//         exportaPopup.style.display = 'none';
//     }
// });



// Abrir pop-up
if (openPopupBtn) {
    openPopupBtn.addEventListener('click', () => {
        popup.style.display = 'flex';
    });
}

function masDetalles(idAdicional){
    popup.style.display = 'flex';
}

// Cerrar pop-up
closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Cerrar pop-up al hacer clic fuera del contenido
// window.addEventListener('click', (e) => {
//     if (e.target === popup) {
//         popup.style.display = 'none';
//     }
// });





function limpiar(){
    document.getElementById('tabla_adicionales').innerHTML = ``;
    selectAllCheckbox.checked = false;
}

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