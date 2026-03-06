/**
 * Sets up the password visibility toggle functionality for the login form.
 */
function setupLoginPasswordToggle() {
    // Select the password toggle button element
    // Assumes the button has the ID 'toggle-login-pass'
    const toggleBtn = document.getElementById('toggle-login-pass');

    // Select the password input field
    // Assumes the input has the ID 'login-password'
    const passwordInput = document.getElementById('login-password');

    // Exit if required elements are not found
    if (!toggleBtn || !passwordInput) {
        console.error("Login password toggle button or input not found.");
        return;
    }

    // Add click event listener to the toggle button
    toggleBtn.addEventListener("click", () => {
        // Check current input type
        const isPasswordHidden = passwordInput.type === "password";

        // Toggle the input type: password <-> text
        passwordInput.type = isPasswordHidden ? "text" : "password";

        // Toggle the button icon/text for visual feedback
        // '⌣' is the "hidden" icon, '👁' is the "visible" icon
        toggleBtn.textContent = isPasswordHidden ? "⌣" : "👁";
    });
}

// Initialize the function once the entire document is loaded
document.addEventListener("DOMContentLoaded", setupLoginPasswordToggle);