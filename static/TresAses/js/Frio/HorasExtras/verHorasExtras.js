const ComboxCentrosCostos = document.getElementById("ComboxCentrosCostos");

const desde = document.getElementById('fechaBusquedaDesde');

const hasta = document.getElementById('fechaBusquedaHasta');

const busqueda = document.getElementById('idBuscaHoras');

const encabezadoHorasExtras = document.getElementById("encabezado-tabla-hs-ex");

//formRestauraHorasExtras


window.addEventListener("load", async () =>{
    await listarCentrosCostos();
    fechaActual();
});

document.getElementById("idBuscaHoras").addEventListener("click", function() {
    verEstadodeHoras();
});

document.getElementById("restauraFormHorasExtras").addEventListener("click", function() {
    const tablaHorasProcesadas = document.getElementById("tablaVerHorasEmpaque");
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
        confirmationPopup.style.display = "flex";
        encabezadoHorasExtras.style.position = "static";  
    }
});

//confirmacion de eliminar
confirmBtn.addEventListener("click", () => {
    restauraHorasEliminadas();
    confirmationPopup.style.display = "none";
    encabezadoHorasExtras.style.position = "sticky"; 
});

cancelBtn.addEventListener("click", () => {
  confirmationPopup.style.display = "none";
  encabezadoHorasExtras.style.position = "sticky";
});


const restauraHorasEliminadas = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formRestauraHorasExtras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("ver/restaura-horas", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color); 
            verEstadodeHoras();     
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
    }
};









const listarCentrosCostos = async () => {
    openProgressBar();
    try {
        const response = await fetch("autoriza/carga-combox-cc")
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = `<option value="0">TODOS LOS CENTROS</option>`;
            data.Datos.forEach((datos) => {
                listado += `
                <option value="${datos.id}">${datos.cc}</option>
                `;
            });
            //ComboxCentrosCostos.style.display = 'block';
            document.getElementById('ComboxCentrosCostos').innerHTML = listado;
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota,color)  
    }
}


const verEstadodeHoras = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formVerHoras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("ver/listado-horas", options);
        const data = await response.json();
        if(data.Message=="Success"){
            //console.log(data);
            let datos_he = ``;
            data.Datos.forEach((datos) => {
                datos_he += `<tr>
                <td >
                    <input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.ID}"${datos.ID_Estado === '0' ? 'disabled' : ''}>
                </td>
                <td >${datos.Tipo}</td>
                <td >${datos.Legajo}</td>
                <td >${datos.Nombre}</td>
                <td >${datos.CC}</td>
                <td >${datos.Desde}</td>
                <td >${datos.Hasta}</td>
                <td >${datos.Motivo}</td>
                <td >${datos.Horas}</td>
                <td >${datos.Dispositivo}</td>
                <td >${datos.Estado}</td>
              </tr>`
            });
            document.getElementById('tablaVerHorasEmpaque').innerHTML = datos_he;
            closeProgressBar();
        }else {
            document.getElementById('tablaVerHorasEmpaque').innerHTML = ``;
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        //console.log(error)
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color); 
    }
};



















































































function fechaActual(){
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
    }, 5000);
}