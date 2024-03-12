


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
    const checkboxes = tablaHorasProcesadas.getElementsByClassName("input-checkbox-hs");
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
        const checkboxes = document.querySelectorAll('.input-checkbox-hs:checked');
        const formData = new FormData();

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const cardDiv = checkbox.closest('tr');
                const cantHorasInput = cardDiv.querySelector('.cant-horas');
                const tipoHoraExtraSelect = cardDiv.querySelector('.tipo-hora-extra');

                if (cantHorasInput && tipoHoraExtraSelect) {
                    const cantHoras = cantHorasInput.value;
                    const tipoHoraExtra = tipoHoraExtraSelect.value;

                    // Agregar los datos al objeto FormData
                    formData.append('idCheck', checkbox.value);
                    formData.append('cantHoras', cantHoras);
                    formData.append('tipoHoraExtra', tipoHoraExtra);
                }
            }
        });


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
                <td>
                    <input class="input-checkbox-hs checkbox" type="checkbox" name="idCheck" value="${datos.ID}">
                </td>
                <td>
                    <select class="selectores tipo-hora-extra" style="max-width: 60px;" name="tipoHoraExtra">
                        <option value="A"${datos.tipo === 'A' ? 'selected' : ''}>A</option>
                        <option value="50"${datos.tipo === '50' ? 'selected' : ''}>50</option>
                        <option value="100"${datos.tipo === '100' ? 'selected' : ''}>100</option>
                        <option value="N"${datos.tipo === 'N' ? 'selected' : ''}>N</option>
                    </select>
                </td>
                <td>${datos.legajo}</td>
                <td>${datos.nombres}</td>
                <td>${datos.desde}</td>
                <td>${datos.hasta}</td>
                <td>
                    <input class="input-number cant-horas" type="number" name="cantHoras" step="0.5" style="max-width: 80px;" value="${datos.horas}">
                </td>
                <td>${datos.descripcion} - ${datos.motivo}</td>
                <td>${datos.centro}</td>
                <td>${datos.solicita}</td>
            </tr>
            `
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
        const checkboxes = document.querySelectorAll(".input-checkbox-hs");
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    } else {
        const checkboxes = document.querySelectorAll(".input-checkbox-hs");
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
    const checkboxes = tablaHorasProcesadas.getElementsByClassName("input-checkbox-hs");
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