// add mask
// CPF
function formatCPF(input) {
    let value = input.value.replace(/\D/g, ''); // remove all non-numbers
    value = value.slice(0, 11); //value limit
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
   
    input.value = value;
}

// phone
function formatPhone(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.slice(0, 12); //value limit
    value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');
    
    input.value = value;
}
