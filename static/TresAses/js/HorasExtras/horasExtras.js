

const ComboxHoras = document.getElementById("formMostrarHorasExtras");
const ComboxLegajos = document.getElementById("formMostrarHorasExtrasLegajo");

const ocultarCombox = () =>{
    ComboxHoras.style.display = 'none';
    ComboxLegajos.style.display = 'none';
}

ComboxBuscarPor.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
        ocultarCombox();
    }else if (selectedValue === 'h') {
        ComboxHoras.style.display = 'block';
        ComboxLegajos.style.display = 'none';
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
        document.getElementById("HeImporte").value = '';
    }else if (selectedValue === 'l') {
        ComboxHoras.style.display = 'none';
        ComboxLegajos.style.display = 'block';
        listarLegajos();
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
        document.getElementById("HeImporte").value = '';
    }
});

ComboxTipoHoraTransf.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
    } else {
        verHorasExtras_transferencia();
    }
});

ComboxTipoLegajoTransf.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
    } else {
        verHorasExtras_transferencia_por_legajos();
    }
});

document.getElementById("enviaElFormHorasExtras").addEventListener("click", function() {
    const heImporteValue = document.getElementById("HeImporte").value;
    const tablaHorasProcesadas = document.getElementById("tablaHorasProcesadas");
    const tieneFilas = tablaHorasProcesadas.getElementsByTagName("tr").length > 0;
    const checkboxes = tablaHorasProcesadas.getElementsByClassName("input-checkbox");
    let alMenosUnTildado = false;
    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            alMenosUnTildado = true;
            break;
        }
    }
    if (!tieneFilas) {
        var message = "Debe buscar horas a enviar.";
        var color = "red";
        mostrarInfo(message,color);
    } else if (heImporteValue === '') {
        var message = "El Importe está vacío. Por favor, ingrese un importe.";
        var color = "red";
        mostrarInfo(message,color);
    }else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un elemento antes de enviar las Horas.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        enviarHorasExtras_transferencia();
    }
});

const modalOverlay = document.querySelector('.modal-overlay');
function openProgressBar() {
  modalOverlay.style.display = 'block';
}
function closeProgressBar() {
  modalOverlay.style.display = 'none';
}



const limpiarCampos = () => {
    document.getElementById('tablaHorasProcesadas').innerHTML = '';
    document.getElementById("HeImporte").value = '';
    document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
    document.getElementById("ComboxBuscarPor").selectedIndex = 0;
    ComboxHoras.style.display = 'none';
    ComboxLegajos.style.display = 'none';
};

const listarLegajos = async () => {
    openProgressBar();
    try {
        const response = await fetch("transferencia/cargar-combox-legajos")
        const data = await response.json();
        if(data.Message=="Success"){
            let legajos_he = `<option value="0">Seleccione</option>`;
            data.Datos.forEach((datos) => {
                legajos_he += `
                <option value="${datos.legajo}">${datos.nombres}</option>
                `;

            });
            document.getElementById('ComboxTipoLegajoTransf').innerHTML = legajos_he;
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        closeProgressBar();
        limpiarCampos(); 
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color)  
    }
}

const verHorasExtras_transferencia_por_legajos = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formMostrarHorasExtrasLegajo");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("transferencia/ver/listado-horas-legajos", options);
        const data = await response.json();
        if(data.Message=="Success" && Array.isArray(data.Datos)){
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `<tr>
                <td style="width: 40px;">
                    <input id="idCheck" name="idCheck" value="${datos.ID}" class="input-checkbox" type="checkbox" ${datos.ID ? 'checked' : ''}>
                </td>
                <td style="width: 60px;">${datos.tipo}</td>
                <td style="width: 80px;">${datos.legajo}</td>
                <td style="width: 280px;">${datos.nombres}</td>
                <td style="width: 180px;">${datos.desde}</td>
                <td style="width: 180px;">${datos.hasta}</td>
                <td>${datos.motivo}</td>
                <td style="width: 80px;">${datos.horas}</td>
              </tr>`
            });
            document.getElementById('tablaHorasProcesadas').innerHTML = datos_he;
            closeProgressBar();
        }else {
            document.getElementById('tablaHorasProcesadas').innerHTML = '';
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        closeProgressBar();
        limpiarCampos(); 
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color); 
    }
};

const verHorasExtras_transferencia = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formMostrarHorasExtras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("transferencia/ver/listado-horas", options);
        const data = await response.json();
        if(data.Message=="Success" && Array.isArray(data.Datos)){
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `<tr>
                <td style="width: 40px;">
                    <input id="idCheck" name="idCheck" value="${datos.ID}" class="input-checkbox" type="checkbox" ${datos.ID ? 'checked' : ''}>
                </td>
                <td style="width: 60px;">${datos.tipo}</td>
                <td style="width: 80px;">${datos.legajo}</td>
                <td style="width: 280px;">${datos.nombres}</td>
                <td style="width: 180px;">${datos.desde}</td>
                <td style="width: 180px;">${datos.hasta}</td>
                <td>${datos.motivo}</td>
                <td style="width: 80px;">${datos.horas}</td>
              </tr>`
            });
            document.getElementById('tablaHorasProcesadas').innerHTML = datos_he;
            closeProgressBar();
        }else {
            document.getElementById('tablaHorasProcesadas').innerHTML = '';
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);
        limpiarCampos();  
    }
};

const enviarHorasExtras_transferencia = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formEnviaHorasExtras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("transferencia/enviar/listado-horas", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            limpiarCampos();
            var color = "green";
            mostrarInfo(nota,color);       
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);
        limpiarCampos();  
    }
};

const eliminaHorasExtras_transferencia = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formEnviaHorasExtras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("transferencia/elimina/listado-horas", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            limpiarCampos();
            var color = "green";
            mostrarInfo(nota,color);       
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);
        limpiarCampos();  
    }
};


/// pop up de confirmación
const encabezadoHorasExtras = document.getElementById("encabezado-tabla-hs-ex");
const showPopupBtn = document.getElementById("showPopupBtn");
const confirmationPopup = document.getElementById("confirmationPopup");
const confirmBtn = document.getElementById("confirmBtn");
const cancelBtn = document.getElementById("cancelBtn");

showPopupBtn.addEventListener("click", () => {
    const tablaHorasProcesadas = document.getElementById("tablaHorasProcesadas");
    const tieneFilas = tablaHorasProcesadas.getElementsByTagName("tr").length > 0;
    const checkboxes = tablaHorasProcesadas.getElementsByClassName("input-checkbox");
    let alMenosUnTildado = false;
    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            alMenosUnTildado = true;
            break;
        }
    }
    if (!tieneFilas) {
        var message = "Debe buscar horas a enviar.";
        var color = "red";
        mostrarInfo(message,color);
    }else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un elemento antes de enviar las Horas.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        confirmationPopup.style.display = "flex";
        encabezadoHorasExtras.style.position = "static";   
    }
  
});

confirmBtn.addEventListener("click", () => {
    eliminaHorasExtras_transferencia();
    confirmationPopup.style.display = "none";
    encabezadoHorasExtras.style.position = "sticky"; 
});

cancelBtn.addEventListener("click", () => {
  confirmationPopup.style.display = "none";
  encabezadoHorasExtras.style.position = "sticky";
});


document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popup").classList.remove("active");
});




function mostrarInfo(Message,Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}





































