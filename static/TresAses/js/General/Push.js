const user = document.getElementById("usuario");
const texto = document.getElementById("texto");




const envía_data = async () => {
    try {
        const formData = new FormData();
        formData.append("User", user.value);
        formData.append("Texto", texto.value);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("envia/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            alert(data.Nota);
        } else {
            alert(data.Nota);
        }
    } catch (error) {
        alert(error);
    }
};
