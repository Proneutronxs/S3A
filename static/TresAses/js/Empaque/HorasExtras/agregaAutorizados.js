/// CONSTANTES!
const ComboxCentrosCostos = document.getElementById("ComboxCentrosCostos");

const fechaPre = document.getElementById('fechaPre');

const fechaAut = document.getElementById('fechaAut');


window.addEventListener("load", async () =>{
    await listarCentrosCostos();
    fechaActual();
});



//// FUNCIONES 
const listarCentrosCostos = async () => {
    openProgressBar();
    try {
        const response = await fetch("autoriza/carga-combox-legajos")
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = `<option value="0">Seleccione</option>`;
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

const Listar_personal = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formCentrosCostosBuscaPersonal");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("agrega/lista-personal", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = ``;
            data.Datos.forEach((datos) => {
                listado += `<tr>
                <td >
                    <input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.Legajo}">
                </td>
                <td >${datos.Legajo}</td>
                <td >${datos.Nombre}</td>
              </tr>`
            });
            document.getElementById('contenidoTablaCentrosCostos').innerHTML = listado;
            closeProgressBar();
        }else {
            document.getElementById('contenidoTablaCentrosCostos').innerHTML = ``;
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
    }
};

ComboxCentrosCostos.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        document.getElementById('contenidoTablaCentrosCostos').innerHTML = '';
        // const miCheckbox = document.getElementById("selectAll");
        // miCheckbox.checked = false;
    } else {
        // const miCheckbox = document.getElementById("selectAll");
        // miCheckbox.checked = false;
        Listar_personal();
    }
});

const guarda_personal_autorizado = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formGuardaPersonalAutorizado");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("agrega/guarda-personal", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            Listar_personal();  
            Listar_personal_Autorizado();  
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
    }
};


document.getElementById("idGuardaPeronal").addEventListener("click", function() {
    const tablaHorasProcesadas = document.getElementById("contenidoTablaCentrosCostos");
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
        var message = "No se encontró Personal.";
        var color = "red";
        mostrarInfo(message,color);
    } else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        guarda_personal_autorizado();
    }
});

const Listar_personal_Autorizado = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formListaPersonalAutorizado");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("agrega/muestra-personal", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = ``;
            data.Datos.forEach((datos) => {
                listado += `<tr>
                <td >
                    <input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.Legajo}">
                </td>
                <td >${datos.Legajo}</td>
                <td >${datos.Nombre}</td>
              </tr>`
            });
            document.getElementById('contenidoTablaAurorizados').innerHTML = listado;
            closeProgressBar();
        }else {
            document.getElementById('contenidoTablaAurorizados').innerHTML = ``;
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color);
        }
    } catch (error) {
        console.log(error)
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color); 
    }
};

const elimina_personal_autorizado = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formListaPersonalAutorizado");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("agrega/elimina-personal", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            Listar_personal();  
            Listar_personal_Autorizado();  
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
    }
};

document.getElementById("idRemovePersonal").addEventListener("click", function() {
    const tablaHorasProcesadas = document.getElementById("contenidoTablaAurorizados");
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
        var message = "No se encontró Personal.";
        var color = "red";
        mostrarInfo(message,color);
    } else if (!alMenosUnTildado) {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        elimina_personal_autorizado();
    }
});

document.getElementById("idBuscaAutorizados").addEventListener("click", function() {
    Listar_personal_Autorizado();
});

function fechaActual(){
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    fechaPre.value = formattedDate;
    fechaAut.value = formattedDate;
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
    }, 6000);
}