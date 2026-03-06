function valid_password() {

    // Gets the input values from the password fields
    let password = document.getElementById("password").value;
    let confirm = document.getElementById("confirm").value;
    let message = document.getElementById("message");

    // Compares both fields and blocks the submit if they differ
    if (password !== confirm) {
        message.textContent = "As senhas não coincidem!";
        return false; // prevents the form submission
    }

    // Clears the message when the passwords match
    message.textContent = "";

    return true; // allows the form submission
}
