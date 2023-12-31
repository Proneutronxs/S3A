


const ComboxLegajosEmpaque = document.getElementById("formMostrarCentrosCostosFrio");

window.addEventListener("load", async () =>{
    await listarCentrosCostosFrio();
});

const listarCentrosCostosFrio = async () => {
    openProgressBar();
    try {
        const response = await fetch("autoriza/carga-combox-cc")
        const data = await response.json();
        if(data.Message=="Success"){
            let legajos_he = `<option value="0">Seleccione</option>`;
            data.Datos.forEach((datos) => {
                legajos_he += `
                <option value="${datos.id}">${datos.cc}</option>
                `;
            });
            ComboxLegajosEmpaque.style.display = 'block';
            document.getElementById('ComboxTipoCCAutorizaFrio').innerHTML = legajos_he;
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color)  
    }
}

document.getElementById("autorizaFormHorasExtras").addEventListener("click", function() {
    const tablaHorasProcesadas = document.getElementById("tablaHorasProcesadasFrio");
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
        var message = "No se encontraron horas.";
        var color = "red";
        mostrarInfo(message,color);
    } else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        enviarHorasExtras_autorizado();
    }
});

const enviarHorasExtras_autorizado = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formEnviaHorasExtrasFrio");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("autoriza/horas-extras", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            verHorasExtras_transferencia_por_cc_Frio();       
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

ComboxTipoCCAutorizaFrio.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        document.getElementById('tablaHorasProcesadasFrio').innerHTML = '';
        const miCheckbox = document.getElementById("selectAll");
        miCheckbox.checked = false;
    } else {
        const miCheckbox = document.getElementById("selectAll");
        miCheckbox.checked = false;
        verHorasExtras_transferencia_por_cc_Frio();
    }
});

const verHorasExtras_transferencia_por_cc_Frio = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formMostrarCentrosCostosFrio");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("autoriza/ver-horas-extras", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `<tr>
                <td >
                    <input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.ID}">
                </td>
                <td >${datos.tipo}</td>
                <td >${datos.legajo}</td>
                <td >${datos.nombres}</td>
                <td >${datos.centro}</td>
                <td >${datos.desde}</td>
                <td >${datos.hasta}</td>
                <td >${datos.motivo} - ${datos.descripcion}</td>
                <td >${datos.horas}</td>
                <td >${datos.solicita}</td>
              </tr>`
            });
            document.getElementById('tablaHorasProcesadasFrio').innerHTML = datos_he;
            closeProgressBar();
        }else {
            document.getElementById('tablaHorasProcesadasFrio').innerHTML = ``;
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







































const selectAllCheckbox = document.getElementById("selectAll");


selectAllCheckbox.addEventListener("change", function () {
    if (selectAllCheckbox.checked) {
        const checkboxes = document.querySelectorAll(".input-checkbox");
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    } else {
        const checkboxes = document.querySelectorAll(".input-checkbox");
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

    }
});

const limpiarCampos = () => {
    document.getElementById('tablaHorasProcesadasFrio').innerHTML = '';
    const miCheckbox = document.getElementById("selectAll");
    miCheckbox.checked = false;
};


const modalOverlay = document.querySelector('.modal-overlay');
function openProgressBar() {
  modalOverlay.style.display = 'block';
}
function closeProgressBar() {
  modalOverlay.style.display = 'none';
}

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
    }, 6000);
}


//boton de eliminar

const encabezadoHorasExtras = document.getElementById("encabezado-tabla-hs-ex");
elminaHEAutoriza.addEventListener("click", () => {
    const tablaHorasProcesadas = document.getElementById("tablaHorasProcesadasFrio");
    const tieneFilas = tablaHorasProcesadas.getElementsByTagName("tr").length > 0;
    const checkboxes = tablaHorasProcesadas.getElementsByClassName("input-checkbox");
    const encabezadoHorasExtras = document.getElementById("encabezado-tabla-hs-ex");
    let alMenosUnTildado = false;
    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            alMenosUnTildado = true;
            break;
        }
    }
    if (!tieneFilas) {
        var message = "No se encontraron horas.";
        var color = "red";
        mostrarInfo(message,color);
    }else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        confirmationPopup.style.display = "flex";
        encabezadoHorasExtras.style.position = "static";   
    }
  
});

//confirmacion de eliminar
confirmBtn.addEventListener("click", () => {
    eliminaHorasExtras_autoriza();
    confirmationPopup.style.display = "none";
    encabezadoHorasExtras.style.position = "sticky"; 
});

cancelBtn.addEventListener("click", () => {
  confirmationPopup.style.display = "none";
  encabezadoHorasExtras.style.position = "sticky";
});


const eliminaHorasExtras_autoriza = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formEnviaHorasExtrasFrio");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("autoriza/elimina/horas-extras", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color); 
            verHorasExtras_transferencia_por_cc_Frio();     
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        console.log(error);
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);
        limpiarCampos();  
    }
};