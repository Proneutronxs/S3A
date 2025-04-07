
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

// const subirAPK = async () => {
//     const form = document.getElementById("formSubirAPK");
//     const formData = new FormData(form);
//     const options = {
//         method: 'POST',
//         body: formData
//     };
    
//     // Lista de URLs a intentar
//     const urls = [
//         "recibir_apk/",             // Primera opción (relativa)
//         "/recibir_apk/",            // Segunda opción (relativa con / inicial)
//         "http://tresasesvpn.ddnsfree.com:8000/api/general/subir-aplicacion/recibir_apk/"  // Tercera opción (absoluta)
//     ];
    
//     for (let i = 0; i < urls.length; i++) {
//         try {
//             console.log(`Intentando con URL: ${urls[i]}`);
//             const response = await fetch(urls[i], options);
            
//             if (!response.ok) {
//                 console.log(`La URL ${urls[i]} respondió con error: ${response.status}`);
//                 continue; // Salta a la siguiente URL si esta falla
//             }
            
//             const data = await response.json();
            
//             if (data.Message == "Success") {
//                 alert(data.Nota);
//             } else {
//                 alert(data.Nota);
//             }
            
//             return; // Sale de la función si tuvo éxito
            
//         } catch (error) {
//             console.error(`Error con URL ${urls[i]}:`, error);
//             // Continúa con la siguiente URL si esta falla
//         }
//     }
//     alert("Se produjo un error al procesar la solicitud con todas las URLs intentadas.");
// };