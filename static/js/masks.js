document.addEventListener("DOMContentLoaded", () => {

    // Apply CEP mask
    function aplicarMascaraCEP(input) {
        input.addEventListener("input", () => {
            let v = input.value.replace(/\D/g, ""); // remove all non-digit characters

            if (v.length > 5) {
                v = v.replace(/(\d{5})(\d)/, "$1-$2"); // adds a dash after the 5th digit
            }

            input.value = v.substring(0, 9); // limits input length to CEP format
        });
    }

    // Apply CPF mask 
    function aplicarMascaraCPF(input) {
        input.addEventListener("input", () => {
            let v = input.value.replace(/\D/g, ""); // remove non-numeric characters

            v = v.replace(/(\d{3})(\d)/, "$1.$2");       // adds first dot
            v = v.replace(/(\d{3})(\d)/, "$1.$2");       // adds second dot
            v = v.replace(/(\d{3})(\d{1,2})$/, "$1-$2"); // adds dash

            input.value = v.substring(0, 14); // limits to full CPF mask size
        });
    }

    // Apply phone mask 
    function aplicarMascaraTelefone(input) {
        input.addEventListener("input", () => {
            let v = input.value.replace(/\D/g, ""); // remove all non-digit characters

            if (v.length > 2) {
                v = v.replace(/(\d{2})(\d)/, "($1) $2"); // adds DDD
            }

            if (v.length > 7) {
                v = v.replace(/(\d{5})(\d)/, "$1-$2");   // adds dash for phone number
            }

            input.value = v.substring(0, 15); // enforces full phone mask size
        });
    }

    // Get field references
    const campoCEP = document.getElementById("end_cep");
    const campoCPF = document.getElementById("input_cpf");
    const campoCel = document.getElementById("input_celular");

    // Apply masks if fields exist
    if (campoCEP) aplicarMascaraCEP(campoCEP);
    if (campoCPF) aplicarMascaraCPF(campoCPF);
    if (campoCel) aplicarMascaraTelefone(campoCel);

});
