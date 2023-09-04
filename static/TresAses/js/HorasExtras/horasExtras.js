

const ComboxHoras = document.getElementById("formMostrarHorasExtras");
const ComboxSectores = document.getElementById("formMostrarHorasExtrasSector");
const ComboxLegajos = document.getElementById("formMostrarHorasExtrasLegajo");
const ComboxFechas = document.getElementById("formMostrarHorasExtrasLegajo");

const ocultarCombox = () =>{
    ComboxHoras.style.display = 'none';
    ComboxLegajos.style.display = 'none';
    ComboxSectores.style.display = 'none';
}

ComboxBuscarPor.addEventListener("change", (event) => {
    document.getElementById("ComboxSectorHEHoras").selectedIndex = 0;
    document.getElementById("ComboxSectorHELegajos").selectedIndex = 0;
    document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
        ocultarCombox();
    }else if (selectedValue === 'h') {
        ComboxSectores.style.display = 'none';
        ComboxHoras.style.display = 'block';
        ComboxLegajos.style.display = 'none';
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
        const miCheckbox = document.getElementById("selectAll");
        miCheckbox.checked = false;
    }else if (selectedValue === 'l') {
        ComboxHoras.style.display = 'none';
        ComboxSectores.style.display = 'block';
        //ComboxHoras.style.display = 'none';
        //ComboxLegajos.style.display = 'block';
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
        const miCheckbox = document.getElementById("selectAll");
        miCheckbox.checked = false;
    }else if (selectedValue == 'f'){
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
        const miCheckbox = document.getElementById("selectAll");
        miCheckbox.checked = false;
        var message = "No disponible.";
        var color = "red";
        mostrarInfo(message,color);
        ocultarCombox();
    }
});

ComboxSectorHEHoras.addEventListener("change", (event) => {
    const miCheckbox = document.getElementById("selectAll");
    miCheckbox.checked = false;
    document.getElementById('tablaHorasProcesadas').innerHTML = '';
    document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
    }else if (selectedValue === 'A') {
        console.log('ADMIN');
    }else if (selectedValue === 'C') {
        console.log('CHACRA');
    }else if (selectedValue === 'E') {
        console.log('EMPAQUE');
    }
});

ComboxSectorHELegajos.addEventListener("change", (event) => {
    document.getElementById('tablaHorasProcesadas').innerHTML = '';
    const miCheckbox = document.getElementById("selectAll");
    miCheckbox.checked = false;
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        limpiarCampos();
    }else if (selectedValue === 'A') {
        console.log('ADMIN');
        ComboxLegajos.style.display = 'block';
        listar_legajos_por_sector();
    }else if (selectedValue === 'C') {
        console.log('CHACRA');
        ComboxLegajos.style.display = 'block';
        listar_legajos_por_sector();
    }else if (selectedValue === 'E') {
        console.log('EMPAQUE');
        ComboxLegajos.style.display = 'block';
        listar_legajos_por_sector();
    }
});

ComboxTipoHoraTransf.addEventListener("change", (event) => {
    const comboxSector = document.getElementById("ComboxSectorHEHoras");
    const selectedIndex = comboxSector.selectedIndex;
    const miCheckbox = document.getElementById("selectAll");
    miCheckbox.checked = false;
    if (selectedIndex == 0){
        var message = "Debe seleccionar un Departamento.";
        var color = "red";
        mostrarInfo(message,color);
        document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
    }else{
        const selectedValue = event.target.value;
        if (selectedValue === '0') {
            document.getElementById('tablaHorasProcesadas').innerHTML = '';
            document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
        } else {
            verHorasExtras_transferencia();
        }
    }
});

ComboxTipoLegajoTransf.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        document.getElementById('tablaHorasProcesadas').innerHTML = '';
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
        var message = "No se encontraron horas.";
        var color = "red";
        mostrarInfo(message,color);
    } else if (heImporteValue === '') {
        var message = "El Importe está vacío.";
        var color = "red";
        mostrarInfo(message,color);
    }else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un item.";
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
    document.getElementById("ComboxTipoHoraTransf").selectedIndex = 0;
    document.getElementById("HeImporte").value = '';
    //document.getElementById("ComboxBuscarPor").selectedIndex = 0;
    ComboxHoras.style.display = 'none';
    ComboxLegajos.style.display = 'none';
};

//FUNCION GET
// const listarLegajos = async () => {
//     openProgressBar();
//     try {
//         const response = await fetch("transferencia/cargar-combox-legajos")
//         const data = await response.json();
//         if(data.Message=="Success"){
//             let legajos_he = `<option value="0">Seleccione</option>`;
//             data.Datos.forEach((datos) => {
//                 legajos_he += `
//                 <option value="${datos.legajo}">${datos.nombres}</option>
//                 `;

//             });
//             document.getElementById('ComboxTipoLegajoTransf').innerHTML = legajos_he;
//             closeProgressBar();
//         }else {
//             closeProgressBar();
//             var nota = data.Nota
//             var color = "red";
//             mostrarInfo(nota,color) 
//         }
//     } catch (error) {
//         closeProgressBar();
//         limpiarCampos(); 
//         var nota = "Se produjo un error al procesar la solicitud.";
//         var color = "red";
//         mostrarInfo(nota,color)  
//     }
// }

const listar_legajos_por_sector = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formMostrarHorasExtrasSector");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("transferencia/cargar-combox-legajos", options);
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
            document.getElementById('ComboxTipoLegajoTransf').innerHTML = ``;
            ComboxLegajos.style.display = 'none';
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);
        limpiarCampos();  
    }
};

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
                    <input id="idCheck" name="idCheck" value="${datos.ID}" class="input-checkbox" type="checkbox">
                </td>
                <td style="width: 60px;">${datos.tipo}</td>
                <td style="width: 80px;">${datos.legajo}</td>
                <td style="width: 280px;">${datos.nombres}</td>
                <td style="width: 180px;">${datos.desde}</td>
                <td style="width: 180px;">${datos.hasta}</td>
                <td style="overflow-x: auto;">${datos.motivo} - ${datos.descripcion}</td>
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
                    <input id="idCheck" name="idCheck" value="${datos.ID}" class="input-checkbox" type="checkbox">
                </td>
                <td style="width: 60px;">${datos.tipo}</td>
                <td style="width: 80px;">${datos.legajo}</td>
                <td style="width: 280px;">${datos.nombres}</td>
                <td style="width: 180px;">${datos.desde}</td>
                <td style="width: 180px;">${datos.hasta}</td>
                <td style="overflow-x: auto; white-space: nowrap;">${datos.motivo} - ${datos.descripcion}</td>
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





































