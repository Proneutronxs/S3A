

const ComboxVer = document.getElementById("ComboxRemitosPor"); //selector de fecha o dia

const FormDesdeHasta = document.getElementById("formTraeRemitosChacrasFecha"); //formulario de busqueda 

const ComboxListRemitos = document.getElementById("ComboxTraeRemitosChacras");//selector de remito por patente y chacra

const EncabezadoA = document.getElementById("encabezado-a");//detalle encabezado

const EncabezadoB = document.getElementById("encabezado-b");//detalle encabezado

const EncabezadoC = document.getElementById("encabezado-c");//detalle encabezado

const TablaDetalle = document.getElementById("Tabla-Detalle-Remito");//detalle de la tabla refreshBusqueda

const Refresh = document.getElementById("refreshBusqueda");

const desdeInput = document.getElementById('desde');

const hastaInput = document.getElementById('hasta');

const overlay = document.getElementById('overlay-remito-nuevo');

const popup = document.getElementById('popup-nuevo-remito');
//overlay-remito-modifica
const popupModifica = document.getElementById('overlay-remito-modifica');

//SPINNERS
const MarcaModifica = document.getElementById('ComboxMarcaBinsModifica');






//TABLA
const tabla = document.getElementById('Tabla-modifica-Remito');
const btnAgrega = document.getElementById('idAgregaBins');
const btnQuita = document.getElementById('idQuitaBins');
const marcaBins = document.getElementById('ComboxMarcaBinsModifica');
const tipoBins = document.getElementById('ComboxTipoBinsModifica');
const cantidadBins = document.getElementById('cantidadBinsModifica');



window.addEventListener("load", async () =>{
    ocultarCombox();
    cargaSpinnerMarcaEspecie();
});

const ocultarCombox = () =>{
    FormDesdeHasta.style.display = 'none';
    ComboxListRemitos.style.display = 'none';
    EncabezadoA.style.display = 'none';
    EncabezadoB.style.display = 'none';
    EncabezadoC.style.display = 'none';
    TablaDetalle.innerHTML = '';
    Refresh.style.display = 'none';

}


ComboxVer.addEventListener("change", (event) => {
    const selectedValue = event.target.value;

    if (selectedValue === '0') {
        ocultarCombox();
    } else if (selectedValue === '1') {
        desdeInput.value = '';
        hastaInput.value = '';

        listar_remitos();
        FormDesdeHasta.style.display = 'none';

        Refresh.style.display = 'block';

        
    } else if (selectedValue === '2') {
        fechaActual();
        ComboxListRemitos.style.display = 'none';
        FormDesdeHasta.style.display = 'block';
        Refresh.style.display = 'none';

        ocultaRemito();
    }
});

ComboxListRemitos.addEventListener("change", (event) => {
    const selectedValue = event.target.value;

    if (selectedValue === '0') {
        EncabezadoA.style.display = 'none';
        EncabezadoB.style.display = 'none';
        EncabezadoC.style.display = 'none';
        TablaDetalle.innerHTML = '';
    } else {
        busca_remito();
    }
});

document.getElementById("buscaRemitosFecha").addEventListener("click", function() {
    listar_remitos();
});

function refreshOnclick(){
    ocultaRemito();
    listar_remitos();
}

function ocultaRemito(){
    EncabezadoA.style.display = 'none';
    EncabezadoB.style.display = 'none';
    EncabezadoC.style.display = 'none';
    TablaDetalle.innerHTML = '';
}

/// METODO PARA BUSCAR EL LISTADO
const listar_remitos = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formTraeRemitosChacrasFecha");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listado-remitos/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let lista_datos = `<option value="0">Seleccione</option>`;
            data.Datos.forEach((datos) => {
                lista_datos += `
                <option value="${datos.ID}">${datos.Detalle}</option>
                `;
            });
            document.getElementById('ComboxTraeRemitosChacras').innerHTML = lista_datos;

            ComboxListRemitos.style.display = 'block';
            Refresh.style.display = 'block'; 
            closeProgressBar();
        }else {
            ComboxListRemitos.style.display = 'none';
            document.getElementById('ComboxTraeRemitosChacras').innerHTML = ``;
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
    }
};

const busca_remito = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formTraeRemitosEncontrados");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("busca-remito/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let encabezado_a = ``;
            let encabezado_b = ``;
            let encabezado_c = ``;
            let detalles = ``;
            data.Datos.forEach((datos) => { 
                encabezado_a += `
                <div class="info-item">
                    <strong>Número Remito:</strong> ${datos.Remito}
                </div>
                <div class="info-item">
                    <strong>Hora:</strong> ${datos.Hora}
                </div>
                <div class="info-item">
                    <strong>Productor:</strong> ${datos.Productor}
                </div>
                <div class="info-item">
                    <strong>Señor:</strong> ${datos.Señor}
                </div>
                <div class="info-item">
                    <strong>Dirección:</strong> ${datos.Direccion}
                </div>
                <div class="info-item">
                    <strong>Renspa:</strong> ${datos.Renspa}
                </div>
                <div class="info-item">
                    <strong>UP:</strong> ${datos.UP}
                </div>
                <div class="info-item">
                    <strong>Capataz:</strong> ${datos.Capataz}
                </div>
                `;
                encabezado_b += `
                <div class="info-item">
                    <strong>Fecha:</strong> ${datos.Fecha}
                </div>
                <div class="info-item">
                    <strong>Especie:</strong> ${datos.Especie}
                </div>
                <div class="info-item">
                    <strong>Variedad:</strong> ${datos.Variedad}
                </div>
                <div class="info-item">
                    <strong>Total Bins:</strong> ${datos.Total}
                </div>
                <div class="info-item">
                    <strong>Chacra:</strong> ${datos.Chacra}
                </div>
                <div class="info-item">
                    <strong>Chofer:</strong> ${datos.Chofer}
                </div>
                <div class="info-item">
                    <strong>Camión:</strong> ${datos.Camion}
                </div>
                <div class="info-item">
                    <strong>Patente:</strong> ${datos.Patente}
                </div>              
                `;
                encabezado_c += `
                <form id="formTraeObservacionRemito" method="POST" action="">
                    <input type="hidden" id="numRemito" name="numRemito" value="${datos.IdRemito}">
                    <input type="hidden" id="idProductor" name="idProductor" value="${datos.IdProductor}">
                    <label for="observaciones">Observaciones:</label><br>
                    <textarea type="text" id="observacionesRemito" name="observacionesRemito" rows="5" placeholder="Datos a modificar.">${datos.Obs}</textarea>
                </form>
                <div class="button-container">
                    <form type="hidden" id="formNuevoRemito" method="POST" action="">
                        <input type="hidden" id="numRemito" name="numRemito" value="${datos.IdRemito}">
                        <input type="hidden" id="idProductor" name="idProductor" value="${datos.IdProductor}">
                    </form>
                    <button id="guardaObservaciones" class="btn-submit botones-remito" type="button" onclick="actualizaObs()">Guardar</button>
                    <button id="modificarRemito" class="btn-submit botones-remito" type="button" onclick="popUpModifica('${datos.IdRemito}','${datos.IdProductor}');">Modificar</button>
                    <button id="descargaRemito" class="btn-submit botones-remito" type="button" onclick="popUpNuevo();">Nuevo</button>
                </div>
                <div class="button-container">
                    <button id="nuevoRemito" class="btn-submit botones-remito-nuevo" type="button" onclick="verRemito()">Descargar</button>
                </div>
                `;

            });
            data.Detalle.forEach((datos) => {
                detalles += `
                <tr>
                    <td>${datos.Cantidad}</td>
                    <td>${datos.Tamaño}</td>
                    <td>${datos.Marca}</td>
                </tr>
                `;
            });

            document.getElementById('encabezado-a').innerHTML = encabezado_a;
            document.getElementById('encabezado-b').innerHTML = encabezado_b;
            document.getElementById('encabezado-c').innerHTML = encabezado_c;
            document.getElementById("Tabla-Detalle-Remito").innerHTML = detalles;
            EncabezadoA.style.display = 'block';
            EncabezadoB.style.display = 'block';
            EncabezadoC.style.display = 'block';
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
        mostrarInfo(nota,color);  
    }
};

function verPdf(remito,productor) {
    var enlace = 'http://192.168.0.2:8000/bascula/remitos-chacras/'
    //var enlace = 'http://tresasesvpn.ddnsfree.com:8000/api/fletes-remitos/data-ver-remito/';
    window.open(enlace, '_blank');
}

const verRemito = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formNuevoRemito");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            body: formData
        };

        const response = await fetch("descarga-pdf/", options);
        if (response.ok) {
            const contentDisposition = response.headers.get('content-disposition');
            const matches = /filename="([^"]+)"/.exec(contentDisposition);
            const fileName = matches ? matches[1] : 'archivo.pdf';

            const blob = await response.blob();

            // Crear un enlace temporal
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);

            // Nombre del archivo sin la extensión
            const fileNameWithoutExtension = fileName.split('.')[0];

            // Nombre final del archivo
            const finalFileName = `${fileNameWithoutExtension}.pdf`;
            link.download = finalFileName.trim();

            // Hacer clic en el enlace y luego eliminarlo
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            var nota = `Error al descargar el PDF: ${response.statusText}`;
            var color = "red";
            mostrarInfo(nota, color);
        }

        closeProgressBar();
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
};

function actualizaObs() {
    const observacionesRemito = document.getElementById("observacionesRemito").value;
    if (!observacionesRemito.trim()) {
        var nota = "El campo de observaciones está vacío.";
        var color = "red";
        mostrarInfo(nota,color) 
    } else {
        actualizaObservaciones();
    }    
}

const actualizaObservaciones = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formTraeObservacionRemito");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("actualiza-obs/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota,color) 
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error)
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

    //const formattedDate = `${dia}/${mes}/${ano}`;
    const formattedDate = `${ano}-${mes}-${dia}`;
    desdeInput.value = formattedDate;
    hastaInput.value = formattedDate;
}


const popUpModifica = async (numero,idProductor) => {
    openProgressBar();
    try {
        const response = await fetch("verifica-modifica/")
        const data = await response.json();
        if(data.Message=="Success"){

            //muestro el pop-up
            popupModifica.style.display = 'block';
            document.getElementById('identificadores-modifica').innerHTML =`
                <input type="hidden" id="numRemitoModifica" name="numRemitoModifica" value="'${numero}'"></input>
                <input type="hidden" id="idProductorModifica" name="idProductorModifica" value="'${idProductor}'"></input>
            `;
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


// Función para agregar una fila a la tabla
function agregarFila() {
    // Verifica que se hayan seleccionado valores válidos
    if (marcaBins.value !== '0' && tipoBins.value !== '0' && cantidadBins.value !== '') {
        // Crea una nueva fila en la tabla
        const newRow = tabla.insertRow();

        // Añade celdas a la fila
        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);

        // Llena las celdas con los valores seleccionados
        cell1.innerHTML = cantidadBins.value;
        cell2.innerHTML = tipoBins.options[tipoBins.selectedIndex].text + '-' + tipoBins.value;
        cell3.innerHTML = marcaBins.options[marcaBins.selectedIndex].text + '-' + marcaBins.value;

        // Reinicia los valores de los controles
        marcaBins.value = '0';
        tipoBins.value = '0';
        cantidadBins.value = '';

        var nota = "Agregado.";
        var color = "green";
        mostrarInfo(nota,color) 
    } else {
        var nota = "Complete los campos.";
        var color = "red";
        mostrarInfo(nota,color) 
    }
}

// Función para quitar la última fila de la tabla
function quitarFila() {
    // Verifica si hay filas en la tabla
    if (tabla.rows.length > 0) {
        // Elimina la última fila
        tabla.deleteRow(-1);
        var nota = "Eliminado.";
        var color = "green";
        mostrarInfo(nota,color); 
    } else {
        var nota = "No hay más filas.";
        var color = "red";
        mostrarInfo(nota,color) 
    }
}

function limpiarTabla() {
    // Elimina todas las filas de la tabla
    while (tabla.rows.length > 0) {
        tabla.deleteRow(0);
    }
}


function ocultarModificaRemito(){
    popupModifica.style.display = 'none';
    limpiarTabla();
}


const popUpNuevo= async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formNuevoRemito");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("verifica-crea-nuevo/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            //muestro overlay y pop-up
            overlay.style.display = 'block';
            popup.style.display = 'block';
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error);
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color)  
    }
}


// const popUpNuevo= async (numero,idProductor) => {
//     openProgressBar();
//     try {
//         const response = await fetch("verifica-nuevo/")
//         const data = await response.json();
//         if(data.Message=="Success"){
//             overlay.style.display = 'block';
//             popup.style.display = 'block';
//             var color = "red";





//             mostrarInfo(numero +"--"+idProductor,color) 
//             closeProgressBar();
//         }else {
//             closeProgressBar();
//             var nota = data.Nota
//             var color = "red";
//             mostrarInfo(nota,color) 
//         }
//     } catch (error) {
//         closeProgressBar();
//         var nota = "Se produjo un error al procesar la solicitud.";
//         var color = "red";
//         mostrarInfo(nota,color)  
//     }
// }


function ocultarNuevoRemito(){
    overlay.style.display = 'none';
    popup.style.display = 'none';
}


/// CARGA SPINNERS DEESPECIE Y MARCA

const cargaSpinnerMarcaEspecie = async () => {
    openProgressBar();
    try {
        const response = await fetch("carga-especie-marca/")
        const data = await response.json();
        if(data.Message=="Success"){
            let seleccion_1 = `<option value="0">MARCA BINS</option>`;
            let seleccion_2 = `<option value="0">ESPECIE</option>`;
            data.DataMarca.forEach((datos) => {
                seleccion_1 += `
                <option value="${datos.idMarca}">${datos.NombreMarca}</option>
                `;
            });
            data.DataEspecie.forEach((datos) => {
                seleccion_2 += `
                <option value="${datos.IdEspecie}">${datos.NombreEspecie}</option>
                `;
            });
            MarcaModifica.innerHTML = seleccion_1;
            document.getElementById('ComboxMarcaBinsNuevo').innerHTML = seleccion_1;
            document.getElementById('ComboxEspecieN').innerHTML = seleccion_2;

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

MarcaModifica.addEventListener("change", (event) => {
    const selectedValue = event.target.value;

    if (selectedValue === '0') {

    } else {
        listar_Envase();
    }
});

const listar_Envase = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formMarcaBinsModifica");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("carga-envase/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            let lista_datos = `<option value="0">ENVASE</option>`;
            data.DataEnvase.forEach((datos) => {
                lista_datos += `
                <option value="${datos.idBins}">${datos.NombreBins}</option>
                `;
            });
            document.getElementById('ComboxTipoBinsModifica').innerHTML = lista_datos;

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
        mostrarInfo(nota,color);  
    }
};

  
const mandaModificacion = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formDatosBinsModifica");
        const formData = new FormData(form);
        console.log(formData);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("actualiza-datos/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            console.log(data)
            closeProgressBar();
        }else {
            closeProgressBar();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error),
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color);  
    }
};

function enviaModificacion(){
    const tablaNoVacia = isTableNotEmpty('Tabla-modifica-Remito');

    if (tablaNoVacia) {
        mandaModificacion();
    } else {
        var nota = "No hay datos cargados.";
        var color = "red";
        mostrarInfo(nota,color);  
    }
}

function isTableNotEmpty(tableId) {
    const table = document.getElementById(tableId);
    
    if (table && table.rows.length > 0) {
        return true;
    } else {
        return false;
    }
}





































document.getElementById("closePopup").addEventListener("click", function() {
    document.getElementById("popup").classList.remove("active");
});

const modalOverlay = document.querySelector('.modal-overlay');
function openProgressBar() {
  modalOverlay.style.display = 'block';
}
function closeProgressBar() {
  modalOverlay.style.display = 'none';
}



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