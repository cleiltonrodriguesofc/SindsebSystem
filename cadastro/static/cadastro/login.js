document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const formButtons = document.querySelector(".form-buttons");

    // Cria um elemento para mostrar erros
    let errorDiv = document.createElement("div");
    errorDiv.className = "login-error";
    errorDiv.style.color = "red";
    errorDiv.style.marginBottom = "10px";
    formButtons.parentNode.insertBefore(errorDiv, formButtons);

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        errorDiv.textContent = ""; // Limpa erros antigos

        const response = await fetch("", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `email=${encodeURIComponent(emailInput.value)}&password=${encodeURIComponent(passwordInput.value)}`
        });

        const data = await response.json();
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            errorDiv.textContent = data.error || "Erro ao tentar logar.";
            passwordInput.value = ""; // Limpa o campo senha para segurança
        }
    });
});
