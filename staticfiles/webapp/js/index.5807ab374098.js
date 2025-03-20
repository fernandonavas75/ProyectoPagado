// Cambiar entre Login y Registro
function showTab(tab) {
    document.getElementById("loginFormContainer").classList.add("hidden");
    document.getElementById("registerFormContainer").classList.add("hidden");
    document.querySelectorAll(".tab").forEach(btn => btn.classList.remove("active"));

    if (tab === "login") {
        document.getElementById("loginFormContainer").classList.remove("hidden");
        document.querySelectorAll(".tab")[0].classList.add("active");
    } else {
        document.getElementById("registerFormContainer").classList.remove("hidden");
        document.querySelectorAll(".tab")[1].classList.add("active");
    }
}

// Manejar Login
document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch("http://localhost:3000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre_usuario: username, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("token", data.token);

        if (data.tipo_usuario === "empleado") {
            window.location.href = "pages/dashboard.html";
        } else {
            window.location.href = "pages/cliente.html";
        }
    } else {
        document.getElementById("loginError").innerText = data.message;
    }
});

// Manejar Registro
document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;
    const role = document.getElementById("registerRole").value;

    const response = await fetch("http://localhost:3000/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre_usuario: username, password, tipo_usuario: role })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Registro exitoso, ahora puedes iniciar sesión.");
        showTab("login");
    } else {
        document.getElementById("registerError").innerText = data.message;
    }
});
