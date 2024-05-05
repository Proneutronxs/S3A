const ComboxCentrosCostos = document.getElementById("ComboxCentrosCostos");

const fechaEnvia = document.getElementById('fechaBusqueda');

const pop_agrega = document.getElementById('pop-agrega');


window.addEventListener("load", async () =>{
    await listarCentrosCostos();
    fechaActual();
});


ComboxCentrosCostos.addEventListener("change", (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === '0') {
        document.getElementById('ContenidoCardHorasExtras').innerHTML = '';
    } else {
        Listar_Horas_Procesadas();
    }
});

const listarCentrosCostos = async () => {
    openProgressBar();
    try {
        const response = await fetch("autoriza/carga-combox-legajos")
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = `<option value="0">SELECCIONE</option>
                <option value="T">TODOS LOS PENDIENTES</option>`;
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

const Listar_Horas_Procesadas = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formHorasDePersonal");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("envia/lista-procesadas", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let listado = ``;
            data.Datos.forEach((datos) => {
                if (datos.DiaNombre === "SÁBADO") {
                    var displayStyle = 'inline';
                } else {
                    var displayStyle = 'none';
                }
                listado += `
                <div class="cardHora">
                    <div class="leftDiv">
                        <div class="horas-item">
                            <input class="input-checkbox-hs checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.ID}">
                            <strong>${datos.Legajo} - ${datos.Nombre} - (${datos.CC} - ${datos.Sindicato})</strong>  
                        </div>
                        <div class="horas-item">
                            <strong>TURNO: </strong>${datos.Turno} 
                            <strong style="margin-left: 7rem;" >HORAS TURNO: </strong>${datos.HorasTurno} 
                        </div>
                        <div class="horas-item">
                            <strong>FICHADA: </strong>${datos.Fichada}
                        </div>
                    </div>
                    <div class="rightDiv">
                        <div class="horas-item">
                            <strong>DÍA: </strong> ${datos.Dia}
                            <strong id="strongElement" style="margin-left: 75px; display: ${displayStyle};"></strong>
                            <button id="boton" onClick="agregaHora(${datos.ID})" class="btn-submit botones bx material-symbols-outlined icon" type="button" style="display: ${displayStyle};">More_time</button>
                        </div>
                        <div class="horas-item">
                            <label class="letras" for="cantHoras">Cant. Horas Extras:</label>
                            <input type="number" class="input-number" step="0.5" id="cantHoras" name="cantHoras" value="${datos.CantHoras}" />
                            <select class="selectores" type="checkbox" id="tipoHoraExtra" name="tipoHoraExtra">
                                <option value="A" ${datos.Tipo === 'A' ? 'selected' : ''}>A</option>
                                <option value="50" ${datos.Tipo === '50' ? 'selected' : ''}>50</option>
                                <option value="100" ${datos.Tipo === '100' ? 'selected' : ''}>100</option>
                            </select>
                        </div>
                    </div>
                </div>
                `;
            });
            document.getElementById('ContenidoCardHorasExtras').innerHTML = listado;
            closeProgressBar();
        } else {
            document.getElementById('ContenidoCardHorasExtras').innerHTML = ``;
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        console.log(error)
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
};


document.getElementById("idActualizaHoras").addEventListener("click", function() {
    var comboxValue = document.getElementById("ComboxCentrosCostos").value;
    if (comboxValue === '0') {
        var message = "Seleccione un Centro de Costo.";
        var color = "red";
        mostrarInfo(message,color);
    } else {
        Listar_Horas_Procesadas();
    }
});

document.getElementById("idEliminaPeronal").addEventListener("click", function() {
    const checkboxes = document.querySelectorAll('#ContenidoCardHorasExtras .input-checkbox-hs');
    const alMenosUnoMarcado = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (alMenosUnoMarcado) {
    elimina_personal_autorizado();
    } else {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    }
});


document.getElementById("idEnviaPeronal").addEventListener("click", function() {
const checkboxes = document.querySelectorAll('#ContenidoCardHorasExtras .input-checkbox-hs');
const alMenosUnoMarcado = Array.from(checkboxes).some(checkbox => checkbox.checked);
if (alMenosUnoMarcado) {
    transfiere_personal();
    } else {
        var message = "Debe seleccionar al menos un item.";
        var color = "red";
        mostrarInfo(message,color);
    }

});

const transfiere_personal = async () => {
    openProgressBar();
    try {
        // Obtener todos los elementos checkbox seleccionados
        const checkboxes = document.querySelectorAll('.input-checkbox-hs:checked');
        
        // Crear un objeto FormData para enviar al servidor
        const formData = new FormData();
        checkboxes.forEach(checkbox => {
            const cardDiv = checkbox.closest('.cardHora');  // Obtener el div cardHora más cercano
            const cantHoras = cardDiv.querySelector('#cantHoras').value;
            const tipoHoraExtra = cardDiv.querySelector('#tipoHoraExtra').value;

            // Agregar los datos al objeto FormData
            formData.append('idCheck', checkbox.value);
            formData.append('cantHoras', cantHoras);
            formData.append('tipoHoraExtra', tipoHoraExtra);
        });

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("envia/tranferir-personal", options);
        const data = await response.json();
        
        if(data.Message == "Success"){
            closeProgressBar();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
            Listar_Horas_Procesadas();
        } else {
            closeProgressBar();
            var nota = data.Nota;
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

const elimina_personal_autorizado = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formTransfiereHorasExtras");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("envia/elimina-personal", options);
        const data = await response.json();
        if(data.Message=="Success"){
            closeProgressBar();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            Listar_Horas_Procesadas();
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



// const transfiere_personal = async () => {
//     openProgressBar();
//     try {
//         const form = document.getElementById("formTransfiereHorasExtras");
//         const formData = new FormData(form);

//         const options = {
//             method: 'POST',
//             headers: {
//             },
//             body: formData
//         };
//         const response = await fetch("envia/tranferir-personal", options);
//         const data = await response.json();
//         if(data.Message=="Success"){
//             closeProgressBar();
//             var nota = data.Nota
//             var color = "green";
//             mostrarInfo(nota,color);
//         }else {
//             closeProgressBar();
//             var nota = data.Nota
//             var color = "red";
//             mostrarInfo(nota,color);
//         }
//     } catch (error) {
//         closeProgressBar();
//         var nota = "Se produjo un error al procesar la solicitud.";
//         var color = "red";
//         mostrarInfo(nota,color);
//     }
// };

const enviaHoraAgregada = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        
        // Agregar campos manualmente al FormData
        formData.append('cantHorasAgrega', document.getElementById('cantHorasAgrega').value);
        formData.append('tipoHoraExtraAgrega', document.getElementById('tipoHoraExtraAgrega').value);
        formData.append('idHoraAgrega', document.getElementById('idHoraAgrega').value);

        const options = {
            method: 'POST',
            headers: {
                // Puedes agregar encabezados personalizados si es necesario
            },
            body: formData
        };
        const response = await fetch("envia/agrega-hora", options);
        const data = await response.json();
        if(data.Message=="Success"){



            closeProgressBar();
            cierraAgrega();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color);
            Listar_Horas_Procesadas();
        }else {
            cierraAgrega();
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
}


function agregaHora(id){
    let idHora = ``;
    idHora += `<input type="hidden" id="idHoraAgrega" name="idHoraAgrega" value="${id}">`;
    document.getElementById('itemIdHora').innerHTML = idHora;

    pop_agrega.style.display = 'block';
}


function cierraAgrega(){
    pop_agrega.style.display = 'none';
}





























































function fechaActual(){
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    fechaEnvia.value = formattedDate;
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