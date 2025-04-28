function validateForm() {
    const name = document.querySelector('#nome').value.trim();
    const cargo = document.querySelector('#cargo').value.trim();
    const email = document.querySelector('#email').value.trim();
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (name === '' || cargo === '') {
        alert('Please fill out all fields.');
        return false;
    }
    if (!email.match(emailPattern)) {
        alert('Invalid email format');
        return false;
    }
    return true;
}

// call function
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#form-cadastrar');
    if (form) {
        form.addEventListener('submit', validateForm);
    }
});



// toggle between enabled and disabled submit button

document.addEventListener("DOMContentLoaded", function () {
    const requiredFieldIds = [
        "nome", "cargo","lotacao", "matricula", "rua", "numero", "bairro",
         "uf", "cidade", "cpf", "rg", "telefone", "email"
    ];


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

    validateFields(); // Caso o navegador complete automaticamente
});


