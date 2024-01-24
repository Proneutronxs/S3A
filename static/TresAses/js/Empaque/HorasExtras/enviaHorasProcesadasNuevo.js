const ComboxCentrosCostos = document.getElementById("ComboxCentrosCostos");

const fechaEnvia = document.getElementById('fechaBusqueda');

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
        if(data.Message=="Success"){
            let listado = ``;
            data.Datos.forEach((datos) => {//${datos.Legajo}
                listado += `
                <div class="cardHora">
                    <div class="leftDiv">
                        <div class="horas-item">
                            <input class="input-checkbox-hs checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.ID}">
                            <strong>${datos.Legajo} - ${datos.Nombre}</strong>  
                        </div>
                        <div class="horas-item">
                            <strong>TURNO: </strong>${datos.Turno} 
                            <strong class="strong-horas">HS. TURNO: </strong>${datos.HorasTurno}
                        </div>
                        <div class="horas-item">
                            <strong>FICHA.: </strong>${datos.Fichada}
                            <strong class="strong-horas">HS. FICHADA: </strong>${datos.HorasFichada}
                        </div>
                    </div>
                    <div class="rightDiv">
                        <div class="horas-item">
                            <strong>TIEMPO EXTRA: </strong> ${datos.TExtra}
                        </div>
                        <div class="horas-item">
                            <label class="letras" for="cantHoras">Cant. Horas Extras:</label>
                            <input type="number" class="input-number" step="0.5" id="cantHoras" name="cantHoras" value="${datos.CantHoras}" />
                            <select class="selectores" type="checkbox" id="tipoHoraExtra" name="tipoHoraExtra">
                                <option value="A">A</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                            </select>
                        </div>
                    </div>
                </div>
                `
            });
            document.getElementById('ContenidoCardHorasExtras').innerHTML = listado;
            closeProgressBar();
        }else {
            document.getElementById('ContenidoCardHorasExtras').innerHTML = ``;
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
        const form = document.getElementById("formListaPersonalAutorizado");
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