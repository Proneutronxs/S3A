
document.getElementById("subirAplicacion").addEventListener("click", function () {
   subirAPK();
});


const subirAPK = async () => {
    try {
        const form = document.getElementById("formSubirAPK");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("recibir_apk/", options);
        const data = await response.json();
        if(data.Message=="Success"){
            var nota = data.Nota
            alert(nota);
        }else {
            var nota = data.Nota
            alert(nota);
        }
    } catch (error) {
        alert("Se produjo un error al procesar la solicitud. " + error);
    }
};