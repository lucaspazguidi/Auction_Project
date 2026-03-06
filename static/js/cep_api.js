document.addEventListener("DOMContentLoaded", () => {

    // Address fields
    const cep = document.getElementById("end_cep");
    const rua = document.getElementById("end_rua");
    const bairro = document.getElementById("end_bairro");
    const cidade = document.getElementById("end_cidade");
    const uf = document.getElementById("end_uf");

    // Blocks the fields initially
    function bloquearCampos() {
        rua.disabled = true;
        bairro.disabled = true;
        cidade.disabled = true;
        uf.disabled = true;
    }

    function liberarCampos() {
        rua.disabled = false;
        bairro.disabled = false;
        cidade.disabled = false;
        uf.disabled = false;
    }

    bloquearCampos();

    // ViaCEP function
    async function buscarCEP(cepLimpo) {
        const cepNumeros = cepLimpo.replace("-", "");

        try {
            const response = await fetch(`https://viacep.com.br/ws/${cepNumeros}/json/`);
            const data = await response.json();

            if (data.erro) {
                alert("CEP not found.");
                bloquearCampos();
                return;
            }

            rua.value = data.logradouro || "";
            bairro.value = data.bairro || "";
            cidade.value = data.localidade || "";
            uf.value = data.uf || "";

            liberarCampos();

        } catch (e) {
            alert("Error fetching CEP. Please try again.");
            bloquearCampos();
        }
    }

    // Mask + trigger for search
    cep.addEventListener("input", () => {
        let v = cep.value.replace(/\D/g, "");
        if (v.length > 5) v = v.replace(/(\d{5})(\d)/, "$1-$2");
        cep.value = v.substring(0, 9);

        if (cep.value.length === 9) {
            buscarCEP(cep.value);
        }
    });

});
