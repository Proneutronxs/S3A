

window.addEventListener("load", async () =>{
    await listarChoferes();
    await listarViajes();
    await listarAsignados();
    await listarRechazados();

    setInterval(async () => {
        await listarChoferes();
    }, 15000);


    setInterval(async () => {
        await listarViajes();
    }, 20000);

    setInterval(async () => {
        await listarRechazados();
    }, 20000);

    setInterval(async () => {
        await listarAsignados();
    }, 20000);

});




const listarChoferes = async () => {
    openProgressBarDisponible();
    try {
        const response = await fetch("listado-choferes/")
        const data = await response.json();
        if(data.Message=="Success"){
            let listado = ``;
            data.Data.forEach((datos) => {
                listado += `
                <div class="cardDisponible">
                    <div class="elementosDisponible">
                        <div class="elemento">${datos.Transporte}</div>
                        <div class="elemento">${datos.Nombre}</div>
                        <div class="elemento">${datos.Actualiza}</div>
                        <div class="disponible" style="background-color: ${datos.HexaDisponible}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Disponible}</div>
                        <div class="libre" style="background-color: ${datos.HexaLibre}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Libre}</div>
                    </div>
                </div>
                `;
            });
            document.getElementById('listado-choferes').innerHTML = listado;
            closeProgressBarDisponible();
        }else {
            closeProgressBarDisponible();
            var nota = data.Nota
            var color = "red";
            //mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error)
        closeProgressBarDisponible();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        //mostrarInfo(nota,color)  
    }
}

const listarViajes = async () => {
    openProgressBarViajes();
    try {
        const response = await fetch("listado-viajes/")
        const data = await response.json();
        console.log(data);
        if(data.Message=="Success"){
            let listado = ``;
            data.Data.forEach((datos) => {
                listado += `
                <div class="cardEnCurso">
                    <div class="elementos">
                        <div class="elemento" style="background-color: #2c89f554;">${datos.Pedido}</div>
                        <div class="elemento">${datos.Transporte}</div>
                        <div class="elemento">${datos.Nombre}</div>
                        <div class="elemento">${datos.Chacra}</div>
                        <div class="elemento" style="background-color: #008f39e7; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Acepta}</div>
                        <div class="elemento" style="background-color: ${datos.HexaRetira}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Retira}</div>
                        <div class="elemento" style="background-color: ${datos.HexaLlega}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Llega}</div>
                        <div class="elemento" style="background-color: ${datos.HexaSale}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Sale}</div>
                        <div class="elemento" style="background-color: ${datos.HexaBascula}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Bascula}</div>
                        <div class="elemento" style="background-color: ${datos.HexaFinaliza}; color: #f1f1f1; border-radius: 2px; width: 100%;">${datos.Finaliza}</div>
                        <div class="data">
                            <button class="btn-actualizar" onclick="openPopup(${datos.ID})">Ubicacion Vacios</button>
                        </div>
                    </div>
                </div>
                `;
            });
            document.getElementById('listado-viajes').innerHTML = listado;
            closeProgressBarViajes();
        }else {
            closeProgressBarViajes();
            var nota = data.Nota
            var color = "red";
            //mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error)
        closeProgressBarViajes();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        //mostrarInfo(nota,color)  
    }
}

const listarAsignados = async () => {
    openProgressBarAsignados();
    try {
        const response = await fetch("listado-asignados/")
        const data = await response.json();
        console.log(data);
        if(data.Message=="Success"){
            let listado = ``;
            data.Data.forEach((datos) => {
                listado += `
                <div class="cardHorizontal">
                    <div class="ladoA">
                        <div class="data">${datos.Flete}</div>
                        <div class="data">${datos.Transporte}</div>
                        <div class="data">${datos.Nombre}</div>
                        <div class="data">${datos.Camion}</div>
                    </div>
                    <div class="ladoB">
                        <div class="data">${datos.Productor}</div>
                        <div class="data">${datos.Chacra}</div>
                        <div class="data">${datos.Zona}</div>
                        <div class="data">
                            <button class="btn-asignar">Aceptar</button>
                            <button class="btn-asignar" onclick="openPopup(${datos.ID})">Ubicacion Vacios</button>
                        </div>
                    </div>
                </div>
                `;
            });
            document.getElementById('listado-asignados').innerHTML = listado;
            closeProgressBarAsignados();
        }else {
            closeProgressBarAsignados();
            var nota = data.Nota
            var color = "red";
            //mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error)
        closeProgressBarAsignados();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        //mostrarInfo(nota,color)  
    }
}

const listarRechazados = async () => {
    openProgressBarRechazados();
    try {
        const response = await fetch("listado-rechazados/")
        const data = await response.json();
        console.log(data);
        if(data.Message=="Success"){
            let listado = ``;
            data.Data.forEach((datos) => {
                listado += `
                <div class="cardHorizontal">
                    <div class="ladoA">
                        <div class="data">${datos.Flete}</div>
                        <div class="data">${datos.Nombre}</div>
                        <div class="data">${datos.Productor}</div>
                        <div class="data">${datos.Chacra}</div>
                    </div>
                    <div class="ladoB">
                        <div class="data">‎ </div>
                        <div class="data">‎ </div>
                        <div class="data">‎ </div>
                        <div class="data">
                            <button class="btn-asignar">Eliminar</button>
                        </div>
                    </div>
                </div>
                `;
            });
            document.getElementById('listado-rechazados').innerHTML = listado;
            closeProgressBarRechazados();
        }else {
            closeProgressBarRechazados();
            var nota = data.Nota
            var color = "red";
            //mostrarInfo(nota,color) 
        }
    } catch (error) {
        console.log(error)
        closeProgressBarRechazados();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        //mostrarInfo(nota,color)  
    }
}




function openPopup(idPedidoFlete) {
    document.getElementById('popupContainer').style.display = 'flex';
    document.getElementById('idPedidoFlete').textContent = idPedidoFlete;
}

function closePopup() {
    document.getElementById('popupContainer').style.display = 'none';
}

function submitPopup() {
    closePopup(); 
}

const progressBarDisponible = document.getElementById('loading-disponible');
function openProgressBarDisponible() {
    progressBarDisponible.style.display = 'flex';
}
function closeProgressBarDisponible() {
    progressBarDisponible.style.display = 'none';
}
const progressBarViajes = document.getElementById('loading-viajes');
function openProgressBarViajes() {
    progressBarViajes.style.display = 'flex';
}
function closeProgressBarViajes() {
    progressBarViajes.style.display = 'none';
}

const progressBarAsignados = document.getElementById('loading-asignados');
function openProgressBarAsignados() {
    progressBarAsignados.style.display = 'flex';
}
function closeProgressBarAsignados() {
    progressBarAsignados.style.display = 'none';
}
const progressBarRechazados = document.getElementById('loading-rechazados');
function openProgressBarRechazados() {
    progressBarRechazados.style.display = 'flex';
}
function closeProgressBarRechazados() {
    progressBarRechazados.style.display = 'none';
}