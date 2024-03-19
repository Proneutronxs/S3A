const desde = document.getElementById('fechaBusquedaDesde');

const hasta = document.getElementById('fechaBusquedaHasta');


window.addEventListener("load", async () =>{
    cargarSelector();
    cargarSelectorChacra();
});


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

//                 // Sumar la cantidad de bins
//                 const totalBins = datos.reduce((acc, curr) => acc + curr, 0);

//                 // Crear el objeto de datos para el gráfico
//                 const data = {
//                     labels: labels,
//                     datasets: [{
//                         label: `${tipoFruta} (${totalBins} - Bins)`, // Tipo de fruta con la cantidad de bins
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
                        },
                        plugins: {
                            afterDraw: (chart) => {
                                const { ctx, chartArea, scales: { y } } = chart;
                                ctx.save();
                                ctx.fillStyle = 'black';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'middle';
                                data.datasets.forEach(dataset => {
                                    for (let i = 0; i < dataset.data.length; i++) {
                                        const model = dataset._meta[Object.keys(dataset._meta)[0]].data[i]._model;
                                        const yScale = y.getPixelForValue(dataset.data[i]);
                                        ctx.fillText(dataset.data[i], model.x, yScale - 10);
                                    }
                                });
                                ctx.restore();
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
    cargarSelector();
    muestraResultados();
});

ComboxVariedad.addEventListener("change", (event) => {
    muestraResultados();
});

ComboxChacra.addEventListener("change", (event) => {
    muestraResultados();
});



function cargarSelector() {
    const especieSelect = document.getElementById('ComboxEspecie');
    const variedadSelect = document.getElementById('ComboxVariedad');

    // Limpia el selector de variedad
    variedadSelect.innerHTML = '';

    // Verifica la opción seleccionada en el selector de especie
    const especieSeleccionada = especieSelect.value;

    // Define los JSON de ejemplo para cada especie
    const manzanaOptions = [
        {value: "", text: "TODO"},
        {value: "102", text: "GALAXI"},
        {value: "26", text: "GOLDEN DELICIOUS"},
        {value: "27", text: "GRANNY SMITH"},
        {value: "30", text: "ITAL RED"},
        {value: "31", text: "KING OREGON"},
        {value: "34", text: "RED CHIEF"},
        {value: "33", text: "RED DELICIOUS"},
        {value: "35", text: "RED MEJORADA"},
        {value: "37", text: "RED STARKRIMSON"},
        {value: "83", text: "ROJA INDUSTRIA"},
        {value: "40", text: "ROYAL GALA"}
    ];

    const peraOptions = [
        {value: "", text: "TODO"},
        {value: "48", text: "ABATE FETEL"},
        {value: "50", text: "BEURRE BOSC"},
        {value: "51", text: "BEURRE DANJOU"},
        {value: "106", text: "GOLDEN RUSSET BOSC"},
        {value: "57", text: "PACKHAMS TRIUMPH"},
        {value: "957", text: "PACKHAMS TRIUMPH F.COND"},
        {value: "85", text: "PERA INDUSTRIA"},
        {value: "58", text: "RED BARTLETT"},
        {value: "59", text: "RED DANJOU"},
        {value: "63", text: "WILLIAMS"}
    ];

    // Carga las opciones según la especie seleccionada
    let opciones;
    if (especieSeleccionada === '1') {
        opciones = manzanaOptions;
    } else if (especieSeleccionada === '2') {
        opciones = peraOptions;
    }

    // Agrega las opciones al selector de variedad
    opciones.forEach(opcion => {
        const option = document.createElement('option');
        option.value = opcion.value;
        option.textContent = opcion.text;
        variedadSelect.appendChild(option);
    });
}


function cargarSelectorChacra() {
    const selectorChacra = document.getElementById('ComboxChacra');
    
    selectorChacra.innerHTML = '';
    
    const opciones = [{value: "", text: "TODO"},
    {value: "1000465", text: "312 ZUCH - GRISANTI S"},
    {value: "1000653", text: "313A - GRISANTI S"},
    {value: "1000656", text: "313B - MOSCARDI F"},
    {value: "1000732", text: "ALLENDE LA ANTOLA - TRES ASES"},
    {value: "1000731", text: "ALLENDE LA FLOR - TRES ASES"},
    {value: "1000729", text: "ALLENDE VM1 - TRES ASES"},
    {value: "1000730", text: "ALLENDE VM2 - TRES ASES"},
    {value: "1000828", text: "BELICH - TRES ASES"},
    {value: "1001058", text: "BEZICH 209 - TRES ASES"},
    {value: "1000760", text: "BIZTESNIK - TRES ASES"},
    {value: "1001001", text: "CAMPETELLA - PIERDOMINI"},
    {value: "1000959", text: "CARIZA CINCO SALTOS - TRES ASES"},
    {value: "1000960", text: "CARIZA PICADA 20 - TRES ASES"},
    {value: "1001102", text: "CEDRO 1 - SANCHEZ OM"},
    {value: "1001059", text: "CEDRO 1 - SUC. DE SA"},
    {value: "1001061", text: "CENTENARIO S/N - SUC. DE SA"},
    {value: "1001071", text: "CH S/N - DELLA GASP"},
    {value: "1001094", text: "CHACRA 301A - TRES ASES"},
    {value: "1001093", text: "CHACRA 301B - TRES ASES"},
    {value: "1001098", text: "CHACRA 302 - TRES ASES"},
    {value: "1001090", text: "CHACRA 303 - TRES ASES"},
    {value: "1001097", text: "CHACRA 304 - TRES ASES"},
    {value: "1001091", text: "CHACRA 313 - TRES ASES"},
    {value: "1001100", text: "CHACRA 317 VILLA REGINA - TRES ASES"},
    {value: "1001092", text: "CHACRA 77 - TRES ASES"},
    {value: "1000772", text: "CHACRA 8 - SAGREDO SE"},
    {value: "1000958", text: "CHACRA 9 - SAGREDO EZ"},
    {value: "1001047", text: "CHACRA DIAZ - PIERDOMINI"},
    {value: "1000978", text: "CHACRA EMILIANO SOLANA - TRES ASES"},
    {value: "1001049", text: "CHACRA JULI - SAGREDO CA"},
    {value: "1001095", text: "CHACRA LA CARMEN - TRES ASES"},
    {value: "1000974", text: "CHCRA 196 - BERTOLDI J"},
    {value: "1000044", text: "CINCO SALTOS - AGROPECUAR"},
    {value: "1001062", text: "CIPOLLETTI 0 - SUC. DE SA"},
    {value: "1001101", text: "CIPOLLETTI 1 - ANDURIL SA"},
    {value: "1001099", text: "CORDERO - ANDURIL SA"},
    {value: "1001064", text: "DALLA PRIA 205 - TRES ASES"},
    {value: "1001065", text: "DALLA PRIA 216 - TRES ASES"},
    {value: "1001054", text: "DALLA PRIA 340 - TRES ASES"},
    {value: "1000982", text: "DIAZ CHACRA 00106 - TRES ASES"},
    {value: "1000762", text: "DIMASI (LA RENACIENTE) - TRES ASES"},
    {value: "1000761", text: "DIMASI 1 (LA COSTA) - TRES ASES"},
    {value: "1001035", text: "GARCIA G - CHACRA 36 - TRES ASES"},
    {value: "1001036", text: "GARCIA G - CHACRA 38 - TRES ASES"},
    {value: "1001040", text: "GARCIA N - ISLA 19 BIS - TRES ASES"},
    {value: "1001086", text: "GOBI - PIERDOMINI"},
    {value: "1000801", text: "HERRERA - TRES ASES"},
    {value: "1001084", text: "HONORATO - TRES ASES"},
    {value: "1001033", text: "JEDREJCIC - CHACRA 205 - TRES ASES"},
    {value: "1000806", text: "LA ESPERANZA 1 - MEO MARTIN"},
    {value: "1000807", text: "LA ESPERANZA 2 - MEO MARTIN"},
    {value: "1000748", text: "LA MAYORINA PIRRELLO - TRES ASES"},
    {value: "1000849", text: "LE MARCHE - TRES ASES"},
    {value: "1000847", text: "LOBRECICH Nº 0234 - TRES ASES"},
    {value: "1000848", text: "LOBRECICH Nº 61 - TRES ASES"},
    {value: "1000981", text: "LOMBI ELIO CHACRA 57 A - TRES ASES"},
    {value: "1001042", text: "LOMBI JC - EX CAUTON - TRES ASES"},
    {value: "1001041", text: "LOMBI JC - LOTE 63 - TRES ASES"},
    {value: "1001044", text: "LOMBI LJ - MARIA ELVIRA - TRES ASES"},
    {value: "1000509", text: "LOTE 1 - ARTERO EDU"},
    {value: "1000753", text: "LOTE 1 - COSTANTINI"},
    {value: "1000422", text: "LOTE 1 - GENNARI OM"},
    {value: "1000001", text: "LOTE 1 - ROM - MIK"},
    {value: "1000010", text: "LOTE 1 - TRES ASES"},
    {value: "1000957", text: "LOTE 1 COSTA - SAGREDO CA"},
    {value: "1000009", text: "LOTE 10 - TRES ASES"},
    {value: "1000026", text: "LOTE 100 (CUNTI) - TRES ASES"},
    {value: "1000015", text: "LOTE 11 A (PIROZZO) - TRES ASES"},
    {value: "1000652", text: "LOTE 11 B - TRES ASES"},
    {value: "1000627", text: "LOTE 12 - BOHIGUES F"},
    {value: "1000016", text: "LOTE 12 - TRES ASES"},
    {value: "1000017", text: "LOTE 13 - TRES ASES"},
    {value: "1000018", text: "LOTE 14 - TRES ASES"},
    {value: "1000019", text: "LOTE 15 - TRES ASES"},
    {value: "1000956", text: "LOTE 16 - SAGREDO SE"},
    {value: "1000916", text: "LOTE 18 - TRES ASES"},
    {value: "1000917", text: "LOTE 19 - TRES ASES"},
    {value: "1000021", text: "LOTE 45/48 - TRES ASES"},
    {value: "1000022", text: "LOTE 46 - TRES ASES"},
    {value: "1000805", text: "LOTE 47 - TRES ASES"},
    {value: "1000011", text: "LOTE 5 - TRES ASES"},
    {value: "1000031", text: "LOTE 50 (CUNTI) - TRES ASES"},
    {value: "1000012", text: "LOTE 6 - TRES ASES"},
    {value: "1000013", text: "LOTE 7 - TRES ASES"},
    {value: "1000008", text: "LOTE 8 - TRES ASES"},
    {value: "1000827", text: "LOTE 80 - WIND FRUITS - TRES ASES"},
    {value: "1000014", text: "LOTE 9 - TRES ASES"},
    {value: "1000846", text: "LUDMAN VIDAL - ANITA - TRES ASES"},
    {value: "1001023", text: "MARQUEZ CHACRA 417 - TRES ASES"},
    {value: "1001066", text: "MARTINEZ 306 - TRES ASES"},
    {value: "1001067", text: "MARTINEZ 307 B - TRES ASES"},
    {value: "1001068", text: "MARTINEZ 308 - TRES ASES"},
    {value: "1001017", text: "MARTINEZ 392 - TRES ASES"},
    {value: "1001015", text: "MARTINEZ CHACRA 305 - TRES ASES"},
    {value: "1001016", text: "MARTINEZ CHACRA 307A - TRES ASES"},
    {value: "1001019", text: "PACHER - LA ELISA - TRES ASES"},
    {value: "1001018", text: "PACHER - LA PARRA - TRES ASES"},
    {value: "1001103", text: "PALOMA - SANCHEZ OM"},
    {value: "1001060", text: "PALOMA - SUC. DE SA"},
    {value: "1000048", text: "PICADA 19 - AGROPECUAR"},
    {value: "1000768", text: "PIRUANA - ARTERO EDU"},
    {value: "1001080", text: "PREISS 2 - TRES ASES"},
    {value: "1001081", text: "PREISS 3 - TRES ASES"},
    {value: "1000899", text: "RAMONDA - PIERDOMINI"},
    {value: "1001003", text: "REENCUENTRO - PIERDOMINI"},
    {value: "1001105", text: "RODRIGUEZ CHACRA 40B - TRES ASES"},
    {value: "1001106", text: "RODRIGUEZ CHACRA 40C - TRES ASES"},
    {value: "1000999", text: "ROSALES - TRES ASES"},
    {value: "1001031", text: "SAN GABRIEL - PIERDOMINI"},
    {value: "1001083", text: "SCRINGER 71 - TRES ASES"},
    {value: "1001038", text: "SUC. GARCIA - ISLA 19 - TRES ASES"},
    {value: "1001076", text: "TENIS - PIERDOMINI"}];
    
    opciones.forEach(opcion => {
        const option = document.createElement('option');
        option.value = opcion.value;
        option.textContent = opcion.text;
        selectorChacra.appendChild(option);
    });
}

  











































































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