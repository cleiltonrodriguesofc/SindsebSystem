document.addEventListener("DOMContentLoaded", function () {
    const requiredFieldIds = [
        "nome", "cargo", "lotacao", "secretaria", "matricula", "rua",
        "numero", "bairro", "uf", "cidade", "cep", "data_nasc",
        "rg", "cpf", "telefone", "email", "data_admissao", "data_socio"
    ];

    const form = document.getElementById("form-cadastrar");
    const submitButton = document.getElementById("submit");

    function validateFields() {
        const allFilled = requiredFieldIds.every(id => {
            const el = document.getElementById(id);
            return el && el.value.trim() !== "";
        });
        submitButton.disabled = !allFilled;
    }

    requiredFieldIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener("input", validateFields);
    });

    validateFields(); // Handle autofill

    form.addEventListener("submit", function (e) {
        const email = document.getElementById("email").value.trim();
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        if (!email.match(emailPattern)) {
            alert("Formato de email inválido.");
            e.preventDefault();
            return false;
        }
    });
});
