document.querySelector('.vr-contenedor-data').style.top = document.querySelector('.vr-fila-3') ? '9rem' : '6rem';
const desde = document.getElementById('vr-fecha-desde');
const hasta = document.getElementById('vr-fecha-hasta');
const loadingContainer = document.getElementById('loading-container');
const displayGeneral = document.getElementById('id-contenedor-empresas');

window.addEventListener("load", async () => {
    fechaActual();
    dataInicial();
});

document.getElementById('busqueda-button').addEventListener('click', function () {
    displayGeneral.style.visibility = 'hidden';
    //dataDateTable();
});

document.getElementById('descargar-button').addEventListener('click', function () {
    //descargarArchivo();
});

selector_productores.addEventListener("change", (event) => {
    dataSubItems();
});

const choiceProductor = new Choices('#selector_productores', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE PRODUCTOR',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceChacra = new Choices('#selector_chacras', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE CHACRA',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choicePersonal = new Choices('#selector_personal', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE PERSONAL',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceLabor = new Choices('#selector_labores', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE LABOR',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceEncargado = new Choices('#selector_encargados', {
    allowHTML: true,
    shouldSort: false,
    placeholderValue: 'SELECCIONE ENCARGADO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const dataInicial = async () => {
    openLoading();
    try {
        const response = await fetch("data-inicial/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Productores.forEach((datos) => {
                result.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });
            choiceProductor.clearChoices();
            choiceProductor.removeActiveItems();
            choiceProductor.setChoices(result, 'value', 'label', true);

            let result2 = [];
            result2.push();
            data.Personal.forEach((datos) => {
                result2.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });
            choicePersonal.clearChoices();
            choicePersonal.removeActiveItems();
            choicePersonal.setChoices(result2, 'value', 'label', true);

            let result3 = [];
            result3.push();
            data.Labores.forEach((datos) => {
                result3.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });
            choiceLabor.clearChoices();
            choiceLabor.removeActiveItems();
            choiceLabor.setChoices(result3, 'value', 'label', true);

            let result4 = [];
            result4.push();
            data.Encargados.forEach((datos) => {
                result4.push({
                    value: datos.Codigo, label: datos.Descripcion
                });
            });
            choiceEncargado.clearChoices();
            choiceEncargado.removeActiveItems();
            choiceEncargado.setChoices(result4, 'value', 'label', true);
        } else {
            choiceProductor.clearChoices();
            choiceProductor.removeActiveItems();
            choicePersonal.clearChoices();
            choicePersonal.removeActiveItems();
            choiceLabor.clearChoices();
            choiceLabor.removeActiveItems();
            choiceEncargado.clearChoices();
            choiceEncargado.removeActiveItems();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const dataSubItems = async () => {
    openLoading();
    try {
        const formData = new FormData();
        formData.append("IdProductor", getValuesProductor());
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("chacra-productor/", options);
        const data = await response.json();
        if (data.Message == "Not Authenticated") {
            window.location.href = data.Redirect;
        } else if (data.Message == "Success") {
            let result = [];
            result.push();
            data.Chacras.forEach((datos) => {
                result.push({ value: datos.IdChacra, label: datos.Descripcion });
            });
            choiceChacra.clearChoices();
            choiceChacra.removeActiveItems();
            choiceChacra.setChoices(result, 'value', 'label', true);
        } else {
            choiceChacra.clearChoices();
            choiceChacra.removeActiveItems();
        }
        closeLoading();
    } catch (error) {
        closeLoading();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

















































































function getValuesProductor() {
    return choiceProductor.getValue() ? choiceProductor.getValue().value : '';
}

function fechaActual() {
    var fecha = new Date();
    var mes = fecha.getMonth() + 1;
    var dia = fecha.getDate();
    var ano = fecha.getFullYear();
    if (dia < 10) dia = '0' + dia;
    if (mes < 10) mes = '0' + mes;
    const formattedDate = `${ano}-${mes}-${dia}`;
    const formattedDateDesde = `${ano}-${'01'}-${'01'}`;
    desde.value = formattedDateDesde;
    hasta.value = formattedDate;
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

function openLoading() {
    loadingContainer.style.display = 'flex';
}

function closeLoading() {
    loadingContainer.style.display = 'none';
}