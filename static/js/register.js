const form = document.getElementById("register-form");

const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const celInput = document.getElementById("input_celular");
const password = document.getElementById("password");
const confirm = document.getElementById("confirm");

const errorName = document.getElementById("error-name");
const errorEmail = document.getElementById("error-email");
const errorCel = document.getElementById("error-cel");
const errorPassword = document.getElementById("error-password");
const errorConfirm = document.getElementById("error-confirm");

const strengthFill = document.getElementById("strength-fill");
const strengthText = document.getElementById("strength-text");

// Utility helpers (visual state)
function setFieldState(input, isValid) {
    input.style.border = isValid ? "2px solid #4CAF50" : "2px solid red";
}

function setValid(input, errorEl) {
    setFieldState(input, true);
    errorEl.textContent = "";
}

function setInvalid(input, errorEl, msg) {
    setFieldState(input, false);
    errorEl.textContent = msg;
}

// Clears all old backend errors before new submission
function clearClientErrors() {
    [errorName, errorEmail, errorCel, errorPassword, errorConfirm].forEach(e => e.textContent = "");
    [nameInput, emailInput, celInput, password, confirm].forEach(i => {
        i.classList.remove("input-error-highlight");
    });
}

// Name validation
function validateName() {
    nameInput.classList.remove("input-error-highlight");

    const value = nameInput.value.trim();
    if (value.length < 3) {
        setInvalid(nameInput, errorName, "Nome muito curto.");
        return false;
    }
    setValid(nameInput, errorName);
    return true;
}
nameInput.addEventListener("input", validateName);

// Email validation
function validateEmail() {
    emailInput.classList.remove("input-error-highlight");

    const value = emailInput.value.trim();
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

    if (!valid) {
        setInvalid(emailInput, errorEmail, "E-mail inválido.");
        return false;
    }
    setValid(emailInput, errorEmail);
    return true;
}
emailInput.addEventListener("input", validateEmail);

// Phone format + soft validation
function validateCel() {
    celInput.classList.remove("input-error-highlight");

    // Cleans and rebuilds masked phone
    let v = celInput.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length === 0) celInput.value = "";
    else if (v.length <= 2) celInput.value = `(${v}`;
    else if (v.length <= 7) celInput.value = `(${v.slice(0,2)}) ${v.slice(2)}`;
    else celInput.value = `(${v.slice(0,2)}) ${v.slice(2,7)}-${v.slice(7)}`;

    // Hard validation only when complete (11 digits)
    if (v.length === 11) {
        setValid(celInput, errorCel);
        return true;
    }

    // While typing, keeps neutral state
    celInput.style.border = "2px solid #ccc";
    errorCel.textContent = "";
    return false;
}
celInput.addEventListener("input", validateCel);
celInput.addEventListener("blur", validateCel);

// Password strength bar
function updateStrength(pass) {
    let score = 0;

    if (pass.length >= 6) score++;
    if (pass.length >= 10) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[!@#$%&*?]/.test(pass)) score++;

    const width = (score / 5) * 100;
    strengthFill.style.width = width + "%";

    // Sets color + label
    if (score <= 1) {
        strengthFill.style.background = "red";
        strengthText.textContent = "Muito fraca";
    } else if (score === 2) {
        strengthFill.style.background = "orangered";
        strengthText.textContent = "Fraca";
    } else if (score === 3) {
        strengthFill.style.background = "orange";
        strengthText.textContent = "Média";
    } else if (score === 4) {
        strengthFill.style.background = "yellowgreen";
        strengthText.textContent = "Boa";
    } else {
        strengthFill.style.background = "green";
        strengthText.textContent = "Forte";
    }
}

// Password validation with feedback of missing parts
function validatePassword() {
    const pass = password.value;
    updateStrength(pass);

    const regexUpper = /[A-Z]/;
    const regexSpecial = /[!@#$%&*?]/;
    const regexNumber = /[0-9]/;

    let errors = [];

    if (pass.length < 6) errors.push(`• Mínimo de 6 caracteres (${6 - pass.length} faltando)`);
    if (!regexUpper.test(pass)) errors.push("• Pelo menos 1 letra maiúscula");
    if (!regexNumber.test(pass)) errors.push("• Pelo menos 1 número");
    if (!regexSpecial.test(pass)) errors.push("• Pelo menos 1 caractere especial (!@#$%&*?)");

    if (errors.length > 0) {
        setInvalid(password, errorPassword, "Senha incompleta:\n" + errors.join("\n"));
        validateConfirmPassword();
        return false;
    }

    setValid(password, errorPassword);
    validateConfirmPassword();
    return true;
}
password.addEventListener("input", validatePassword);

// Password confirmation validation
function validateConfirmPassword() {
    const pass = password.value;
    const conf = confirm.value;

    // Resets visual if both empty
    if (pass === "" && conf === "") {
        confirm.style.border = "2px solid #ccc";
        errorConfirm.textContent = "";
        return false;
    }

    // Cannot confirm an invalid password
    const regex = /^(?=.*[A-Z])(?=.*[!@#$%&*?]).{6,}$/;
    if (!regex.test(pass)) {
        setInvalid(confirm, errorConfirm, "A senha ainda não é válida.");
        return false;
    }

    // Checks match
    if (conf !== pass) {
        setInvalid(confirm, errorConfirm, "As senhas não coincidem.");
        return false;
    }

    setValid(confirm, errorConfirm);
    return true;
}
confirm.addEventListener("input", validateConfirmPassword);

// Enter = go to next input (form navigation)
document.addEventListener("keydown", function(e){
    if (e.key === "Enter") {
        const formEl = e.target.form;
        if (!formEl) return;

        e.preventDefault();
        const index = Array.prototype.indexOf.call(formEl, e.target);
        formEl.elements[index + 1]?.focus();
    }
});

// Password visibility toggle
function setupPasswordToggle(btnId, inputId) {
    const btn = document.getElementById(btnId);
    const input = document.getElementById(inputId);

    if (!btn || !input) return;

    btn.addEventListener("click", () => {
        const isHidden = input.type === "password";
        input.type = isHidden ? "text" : "password";
        btn.textContent = isHidden ? "⌣" : "👁";
    });
}
setupPasswordToggle("toggle-pass", "password");
setupPasswordToggle("toggle-confirm", "confirm");

// Full validation used before fetch submit
function validateForm() {
    const a = validateName();
    const b = validateEmail();
    const c = validateCel();
    const d = validatePassword();
    const e = validateConfirmPassword();

    // cel can be optional depending on your rules
    return a && b && (c || celInput.value.trim() === "") && d && e;
}

// Form submission with fetch (AJAX)
form.addEventListener("submit", async (evt) => {
    evt.preventDefault();

    clearClientErrors();

    if (!validateForm()) return;

    const payload = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        cel: celInput.value.trim(),
        password: password.value,
        confirm: confirm.value
    };

    try {
        const res = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
            credentials: "include"
        });

        const data = await res.json();

        // Handles backend validation errors
        if (data.error) {
            const field = data.field || "name";
            const message = data.message || "Erro no servidor";

            const input = document.getElementById(field);
            if (input) {
                if (input.type !== "password") input.value = "";
                input.focus();
                input.classList.add("input-error-highlight");
            }

            const errEl = document.getElementById(`error-${field}`);
            if (errEl) errEl.textContent = message;

            return;
        }

        // Success → redirect
        if (data.success && data.redirect) {
            window.location.href = data.redirect;
            return;
        }

        // fallback reload
        window.location.reload();

    } catch (err) {
        console.error("Erro ao enviar requisição:", err);
        alert("Ocorreu um erro ao tentar registrar. Tente novamente.");
    }
});
