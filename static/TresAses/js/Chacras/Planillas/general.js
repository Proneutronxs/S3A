

const desde = document.getElementById('fechaInicio');
const hasta = document.getElementById('fechaFinal');
const selectAllCheckbox = document.getElementById('selectAll');
const openPopupBtn = document.getElementById('open-popup');
const popup = document.getElementById('pop_up_detalles');
const closePopupBtn = document.getElementById('close-popup');
const exportaPopup = document.getElementById('exporta-planilla-popup');
const exportaCloseBtn = exportaPopup.querySelector('.exporta-planilla-close-popup');
const popUpPremio = document.getElementById('confirmationPopupPremio');
const archivo = document.getElementById('exporta-planilla-tipo-archivo');

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

document.getElementById('generar_archivo').addEventListener('click', function () {
    if (archivo.value == '0'){
        var nota = "Debe seleccionar un Tipo de Archivo.";
        var color = "red";
        mostrarInfo(nota, color);
    }else {
        descargarArchivo();
    }
});

document.getElementById('addPremio').addEventListener('click', function () {
    var tabla = document.getElementById('tabla_adicionales');
    var checkboxes = tabla.querySelectorAll('input[type="checkbox"]');
    var mostrarError = true;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            premio();
            popUpPremio.style.display = "flex";
            mostrarError = false;
        }
    });
    if (mostrarError) {
        var nota = "Debe seleccionar un Item.";
        var color = "red";
        mostrarInfo(nota, color);
    }
});

document.getElementById('update_importe').addEventListener('click', function () {
    var tabla = document.getElementById('tabla_adicionales');
    var checkboxes = tabla.querySelectorAll('input[type="checkbox"]');
    var mostrarError = true;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            importe();
            popUpPremio.style.display = "flex";
            mostrarError = false;
        }
    });
    if (mostrarError) {
        var nota = "Debe seleccionar un Item.";
        var color = "red";
        mostrarInfo(nota, color);
    }
});

document.getElementById('cancelar_Premio').addEventListener('click', function () {
    popUpPremio.style.display = "none";
});

document.getElementById('cancelar_id').addEventListener('click', function () {
    confirmacion_id.style.display = "none";
});

document.getElementById('confirmar_Premio').addEventListener('click', function () {
    premio_adicionales();
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
                                <td class="texto-end">${datos.ImportePremio}</td>
                                <td class="texto-centro">${datos.Pago}</td>
                                <td class="texto-end">${datos.Importe}</td>
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

const detalleAdicional = async (idAdicional) => {
    try {
        const formData = new FormData();
        formData.append("ID", idAdicional);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("detalle-adicional/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            selectAllCheckbox.checked = false;
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `

                        <div class="popup-columns">
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>ID ADICIONAL:</strong> ${datos.Id}
                                </div>
                                <div class="info-item">
                                    <strong>NOMBRE:</strong> ${datos.Nombre}
                                </div>
                                <div class="info-item">
                                    <strong>CENTRO:</strong> ${datos.Centro}
                                </div>
                                <div class="info-item">
                                    <strong>CATEGORÍA:</strong> ${datos.Categoria}
                                </div>
                                <div class="info-item">
                                    <strong>DESCRIPCIÓN:</strong> ${datos.Descripcion}
                                </div>
                                <div class="info-item">
                                    <strong>TAREA:</strong> ${datos.Tarea}
                                </div>
                                <div class="info-item">
                                    <strong>CANT. DÍAS:</strong> ${datos.Dias}
                                </div>
                            </div>
                            <div class="popup-column">
                                <div class="info-item">
                                    <strong>CANT. UNI.:</strong> ${datos.Cantidad}
                                </div>
                                <div class="info-item">
                                    <strong>TIPO:</strong> ${datos.Tipo}
                                </div>
                                <div class="info-item">
                                    <strong>LOTE:</strong> ${datos.Chacra}
                                </div>
                                <div class="info-item">
                                    <strong>CUADRO:</strong> ${datos.Cuadro}
                                </div>
                                <div class="info-item">
                                    <strong>F. PAGO:</strong> ${datos.Pago}
                                </div>
                                <div class="info-item">
                                    <strong>IMPORTE:</strong> ${datos.Importe}
                                </div>
                                <div class="info-item">
                                    <strong>ENCARGADO:</strong> ${datos.Encargado}
                                </div>
                            </div>
                        </div>
                        <div class="popup-observaciones">
                            <h3>Observaciones</h3>
                            <textarea rows="4" placeholder="Sin Observaciones ..." disabled>
                                    ${datos.Obs}
                            </textarea>
                        </div>
                            `
            });
            document.getElementById('content-detalles-planilla-general').innerHTML = datos_he;
            closeProgressBar();
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

const premio_adicionales = async () => {
    try {
        
        const checkboxes = document.querySelectorAll('.input-checkbox:checked');
        const imput_premio = document.getElementById('imput_importe').value;
        const url = document.getElementById('valor-id').value;
        const formData = new FormData();
        formData.append("Premio",imput_premio)

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

        const response = await fetch(url, options);
        const data = await response.json();
        popUpPremio.style.display = "none";
        if(data.Message=="Success"){
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            completarTablaA();       
        }else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        popUpPremio.style.display = "none";
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota,color);
    }
};

const descargarArchivo = async () => {
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
            headers: {},
            body: formData
        };

        const response = await fetch('crear-archivos/', options);
        const contentType = response.headers.get('content-type');
        
        closeProgressBar();
        exportaPopup.style.display = 'none';

        if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
            const blob = await response.blob();
            const excelURL = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = excelURL;
            a.style.display = 'none';
            a.download = 'Listado Adicionales_' + obtenerFechaHoraActual() + '.xlsx'; 
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(excelURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        popUpPremio.style.display = "none";
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


function importe(){
    document.getElementById('conetnido_importes').innerHTML =  `
    <h4>MODIFICAR EL IMPORTE</h4>
    <div style="margin-top: 20px;" id="contenido_popupPremio">
        <p>Introduzca el importe para los seleccionados.</p>
        <input class="input" id="imput_importe" style=" max-width: 150px; text-align: center;" type="number">
    </div>
    <input type="text" name="valor-id" id="valor-id"  value="inserta-importe-adicionales/" hidden>
    `;
}

function premio(){
    document.getElementById('conetnido_importes').innerHTML =  `
        <h4>IMPORTE PREMIO</h4>
        <div style="margin-top: 20px;" id="contenido_popupPremio">
            <p>Introduzca el importe del Premio para los seleccionados.</p>
            <input class="input" id="imput_importe" style=" max-width: 150px; text-align: center;" type="number">
        </div>
    <input type="text" name="valor-id" id="valor-id"  value="inserta-premio-adicionales/" hidden>
    `;
}

function openExportaPopup() {
    exportaPopup.style.display = 'flex';
}

exportaCloseBtn.addEventListener('click', () => {
    exportaPopup.style.display = 'none';
});

// Cerrar pop-up al hacer clic fuera del contenido
// window.addEventListener('click', (e) => {
//     if (e.target === exportaPopup) {
//         exportaPopup.style.display = 'none';
//     }
// });



if (openPopupBtn) {
    openPopupBtn.addEventListener('click', () => {
        popup.style.display = 'flex';
    });
}

function masDetalles(idAdicional){
    detalleAdicional(idAdicional);
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