

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

window.addEventListener("load", async () =>{
    ocultarCombox();
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
    listar_remitos();
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
                    <button id="guardaObservaciones" class="btn-submit botones-remito" type="button" onclick="actualizaObs()">Guardar</button>
                    <button id="modificarRemito" class="btn-submit botones-remito" type="button" onclick="popUpModifica('${datos.IdRemito}','${datos.IdProductor}');">Modificar</button>
                    <button id="descargaRemito" class="btn-submit botones-remito" type="button" onclick="popUpNuevo('${datos.IdRemito}');">Nuevo</button>
                </div>
                <div class="button-container">
                    <button id="nuevoRemito" class="btn-submit botones-remito-nuevo" type="button" onclick="verPdf('${datos.PDF}')">Descargar</button>
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

function verPdf(nombrePDF) {
    var enlace = 'http://192.168.1.110/api/fletes-remitos/data-ver-remito/' + nombrePDF;
    window.open(enlace, '_blank');
}

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
            var color = "red";
            var nota = numero + ' - - ' + idProductor;
            mostrarInfo(nota,color) 
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


const popUpNuevo= async (numero) => {
    openProgressBar();
    try {
        const response = await fetch("verifica-nuevo/")
        const data = await response.json();
        if(data.Message=="Success"){
            overlay.style.display = 'block';
            popup.style.display = 'block';
            var color = "red";
            mostrarInfo(numero,color) 
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


function ocultarNuevoRemito(){
    overlay.style.display = 'none';
    popup.style.display = 'none';
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