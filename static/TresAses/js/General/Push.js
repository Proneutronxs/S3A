




function enviaData() {
    const archivoInput = document.getElementById('archivo');
    const parametroInput = document.getElementById('parametro');

    if (!archivoInput.files.length) {
        alert('Seleccione un archivo');
        return;
    }

    if (!parametroInput.value.trim()) {
        alert('Ingrese un parámetro');
        return;
    }

    const formData = new FormData();
    formData.append('archivo', archivoInput.files[0]);
    formData.append('parametro', parametroInput.value);

    fetch('sube-archivo/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        alert('Archivo subido correctamente');
    })
    .catch(error => {
        alert('Error al subir archivo: ' + error.message);
    });
}
