




const verificar_Permisos = async (sector) => {
    try {
        const response = await fetch("verificar/permisos&sector=" + sector)
        const data = await response.json();
        if(data.Message=="Success"){
            window.location.href = data.URL;
        }else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota,color) 
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota,color)  
    }
}

function mostrarInfo(Message,Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 3000);
}