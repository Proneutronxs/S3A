const loginButton = document.getElementById("login-button");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

document.getElementById('login-button').addEventListener('click', function() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('ingresar-zetone/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password)
    })
    .then(response => response.json())
    .then(data => {
        if (data.Message == 'Success') {
            window.location.href = '/';
        } else {
            mostrarInfo(data.Nota,"red")
        }
    })
    .catch(error => {
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
    });
});

usernameInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
      loginButton.click();
    }
});

passwordInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
      loginButton.click();
    }
});

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