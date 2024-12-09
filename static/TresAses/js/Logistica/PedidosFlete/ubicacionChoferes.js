let map;
let existe = true;
const modalOverlay = document.querySelector('.modal-overlay');

window.addEventListener("load", async () => {
    listar_choferes();
});

selector_choferes.addEventListener("change", (event) => {
    mapeo_ultima_ubicacion();
});

document.getElementById('pfa-refresh').addEventListener('click', function () {
    mapeo_ultima_ubicacion();
});

document.getElementById('selector_choferes').addEventListener('click', function () {
    oculta_leaflet();
});

const choiceChoferes = new Choices('#selector_choferes', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CHOFER',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const listar_choferes = async () => {
    openProgressBar();
    try {
        const response = await fetch("listar-choferes-activos/");
        const data = await response.json();
        closeProgressBar();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Choferes.forEach((datos) => {
                result.push({
                    value: datos.IdCA,
                    label: datos.Chofer
                })
            });
            choiceChoferes.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const mapeo_ultima_ubicacion = async () => {
    openProgressBar();
    try {
        const formData = new FormData();
        formData.append("ID_CA", getValueChoferes());

        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };

        const response = await fetch("ubicacion-choferes-activos/", options);
        const data = await response.json();
        closeProgressBar();
        if (data.Message == "Success") {
            const mapContainer = document.getElementById('pfa_mapeo_actual_todos');
            mapContainer.style.display = 'block';
            if (map) {
                map.off();
                map.remove();
            }
            const lat = parseFloat(data.Datos[0].Latitud);
            const lng = parseFloat(data.Datos[0].Longitud);
            map = L.map(mapContainer).setView([lat, lng], 12);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

            data.Datos.forEach((driver) => {
                const driverLat = parseFloat(driver.Latitud);
                const driverLng = parseFloat(driver.Longitud);
                const driverIcon = L.divIcon({
                    className: 'custom-icon',
                    html: ` <div class="material-symbols-outlined"
                                style="height: 32px; width: 32px; background-color: white; color: blue; border-radius: 50%; 
                                        display: flex; align-items: center; justify-content: center; 
                                        border: 2px solid black;">
                                local_shipping
                            </div>`,
                    iconSize: [15, 15],
                    iconAnchor: [7, 15],
                    popupAnchor: [0, -30]
                });

                L.marker([driverLat, driverLng], { icon: driverIcon }).addTo(map)
                    .bindPopup(`<strong>${driver.Chofer}</strong><br>${driver.Fecha}`) 
                    .openPopup();

            });

            mapContainer.style.display = 'block';
            existe = false;
        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        closeProgressBar();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

function getValueChoferes() {
    return choiceChoferes.getValue() ? choiceChoferes.getValue().value : '0';
}

function oculta_leaflet() {
    const leaflet = document.getElementById('pfa_mapeo_actual_todos');
    if (!existe) {
        leaflet.style.display = 'none';
    }
}











































function openProgressBar() {
    modalOverlay.style.display = 'block';
}
function closeProgressBar() {
    modalOverlay.style.display = 'none';
}
function mostrarInfo(Message, Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}









































































