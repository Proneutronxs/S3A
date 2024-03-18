const desde = document.getElementById('fechaBusquedaDesde');

const hasta = document.getElementById('fechaBusquedaHasta');















// document.addEventListener('DOMContentLoaded', function() {
//     fechaActual();
//     // Obtener el contexto del lienzo
//     const ctx = document.getElementById('line-chart').getContext('2d');

//     // Definir los datos del gráfico
//     const data = {
//         labels: ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes','Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'],
//         datasets: [{
//             label: 'PERA',
//             data: [1234, 1532, 1224, 1562, 1538, 1238,1586,1485,1234, 1532],
//             borderColor: 'blue',
//             backgroundColor: 'transparent',
//             borderWidth: 2
//         },
//         {
//             label: 'MANZANA',
//             data: [1254, 1632, 1124, 962, 1138, 1038,1786,1885, 1124, 962],
//             borderColor: 'green',
//             backgroundColor: 'transparent',
//             borderWidth: 2
//         }]
//     };

//     // Configurar las opciones del gráfico
//     const options = {
//         scales: {
//             y: {
//                 beginAtZero: true
//             }
//         }
//     };

//     // Crear el gráfico de líneas
//     const lineChart = new Chart(ctx, {
//         type: 'line',
//         data: data,
//         options: options
//     });
// });





// const muestraResultados = async () => {
//     openProgressBar();
//     try {
//         const form = document.getElementById("formEstadisticas");
//         const formData = new FormData(form);

//         const options = {
//             method: 'POST',
//             headers: {},
//             body: formData
//         };
//         const response = await fetch("ver-estadisticas/", options);
//         const dato = await response.json();
//         if(dato.Message === "Success") {
//             closeProgressBar();
//             const ctx = document.getElementById('line-chart').getContext('2d');

//             const dataDatos = JSON.parse(dato.Datos);

//             console.log(dataDatos);
            
//             const tipoFruta = Object.keys(dataDatos)[0]; // Obtener el primer (y único) tipo de fruta
//             const labels = dataDatos[tipoFruta].map(entry => entry.Fecha);
//             const datos = dataDatos[tipoFruta].map(entry => parseInt(entry.Cantidad));

//             // Crear el objeto de datos para el gráfico
//             const data = {
//                 labels: labels,
//                 datasets: [{
//                     label: tipoFruta, // Usar el tipo de fruta como etiqueta del dataset
//                     data: datos,
//                     borderColor: 'blue',
//                     backgroundColor: 'transparent',
//                     borderWidth: 2
//                 }]
//             };
            
//             const options = {
//             scales: {
//                 y: {
//                 beginAtZero: true
//                 }
//             }
//             };
            
//             const lineChart = new Chart(ctx, {
//             type: 'line',
//             data: data,
//             options: options
//             });


//         } else {
//             closeProgressBar();
//             const nota = dato.Nota;
//             const color = "red";
//             mostrarInfo(nota, color);
//         }
//     } catch (error) {
//         console.log(error);
//         closeProgressBar();
//         const nota = "Se produjo un error al procesar la solicitud.";
//         const color = "red";
//         mostrarInfo(nota, color);
//     }
// };



// const muestraResultados = async () => {
//     openProgressBar();
//     try {
//         const form = document.getElementById("formEstadisticas");
//         const formData = new FormData(form);

//         const options = {
//             method: 'POST',
//             headers: {},
//             body: formData
//         };

//         const response = await fetch("ver-estadisticas/", options);
//         const dato = await response.json();

//         if (dato.Message === "Success") {
//             closeProgressBar();

//             const dataDatos = JSON.parse(dato.Datos);

//             // Obtener el contexto del lienzo
//             const canvasContainer = document.getElementById('canvas-container');

//             // Limpiar el contenedor de gráficos
//             canvasContainer.innerHTML = '';

//             // Iterar sobre cada tipo de fruta y crear un gráfico para cada una
//             Object.keys(dataDatos).forEach(tipoFruta => {
//                 const labels = dataDatos[tipoFruta].map(entry => entry.Fecha);
//                 const datos = dataDatos[tipoFruta].map(entry => parseInt(entry.Cantidad));

//                 // Crear el objeto de datos para el gráfico
//                 const data = {
//                     labels: labels,
//                     datasets: [{
//                         label: tipoFruta, // Usar el tipo de fruta como etiqueta del dataset
//                         data: datos,
//                         borderColor: 'blue',
//                         backgroundColor: 'transparent',
//                         borderWidth: 2
//                     }]
//                 };

//                 // Crear un elemento canvas para el gráfico
//                 const canvas = document.createElement('canvas');
//                 canvasContainer.appendChild(canvas);

//                 // Obtener el contexto del lienzo para el gráfico actual
//                 const ctx = canvas.getContext('2d');

//                 // Crear el gráfico de líneas para esta fruta
//                 new Chart(ctx, {
//                     type: 'line',
//                     data: data,
//                     options: {
//                         scales: {
//                             y: {
//                                 beginAtZero: true
//                             }
//                         }
//                     }
//                 });
//             });

//         } else {
//             closeProgressBar();
//             const nota = dato.Nota;
//             const color = "red";
//             mostrarInfo(nota, color);
//         }
//     } catch (error) {
//         console.log(error);
//         closeProgressBar();
//         const nota = "Se produjo un error al procesar la solicitud.";
//         const color = "red";
//         mostrarInfo(nota, color);
//     }
// };

const muestraResultados = async () => {
    openProgressBar();
    try {
        const form = document.getElementById("formEstadisticas");
        const formData = new FormData(form);

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch("ver-estadisticas/", options);
        const dato = await response.json();

        if (dato.Message === "Success") {
            closeProgressBar();

            const dataDatos = JSON.parse(dato.Datos);

            // Obtener el contexto del lienzo
            const canvasContainer = document.getElementById('canvas-container');

            // Limpiar el contenedor de gráficos
            canvasContainer.innerHTML = '';

            // Iterar sobre cada tipo de fruta y crear un gráfico para cada una
            Object.keys(dataDatos).forEach(tipoFruta => {
                const labels = dataDatos[tipoFruta].map(entry => entry.Fecha);
                const datos = dataDatos[tipoFruta].map(entry => parseInt(entry.Cantidad));

                // Sumar la cantidad de bins
                const totalBins = datos.reduce((acc, curr) => acc + curr, 0);

                // Crear el objeto de datos para el gráfico
                const data = {
                    labels: labels,
                    datasets: [{
                        label: `${tipoFruta} (${totalBins} - Bins)`, // Tipo de fruta con la cantidad de bins
                        data: datos,
                        borderColor: 'blue',
                        backgroundColor: 'transparent',
                        borderWidth: 2
                    }]
                };

                // Crear un elemento canvas para el gráfico
                const canvas = document.createElement('canvas');
                canvasContainer.appendChild(canvas);

                // Obtener el contexto del lienzo para el gráfico actual
                const ctx = canvas.getContext('2d');

                // Crear el gráfico de líneas para esta fruta
                new Chart(ctx, {
                    type: 'line',
                    data: data,
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });

        } else {
            closeProgressBar();
            const nota = dato.Nota;
            const color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        console.log(error);
        closeProgressBar();
        const nota = "Se produjo un error al procesar la solicitud.";
        const color = "red";
        mostrarInfo(nota, color);
    }
};



ComboxMes.addEventListener("change", (event) => {
    muestraResultados();
});

ComboxEspecie.addEventListener("change", (event) => {
    muestraResultados();
});

















































































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