document.addEventListener('DOMContentLoaded', () => {

    // Element selection
    const rechargeRadios = document.querySelectorAll('input[name="recharge_amount"]');
    const customRadio = document.getElementById('custom-radio');
    const customField = document.getElementById('custom-amount-field');
    const customInput = document.getElementById('custom_amount');

    const amountOptions = document.querySelectorAll('.amount-option.selectable');

    // Primary color for styling
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary') || '#1D4ED8';


    // Update visual selection state
    function updateSelectedVisuals() {
        amountOptions.forEach(label => {
            const input = label.querySelector('input');
            const buttonSpan = label.querySelector('.amount-btn');

            if (input.checked) {
                buttonSpan.style.backgroundColor = primaryColor;
                buttonSpan.style.color = 'white';
                buttonSpan.style.borderColor = primaryColor;
                buttonSpan.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.15)';
            } else {
                buttonSpan.style.backgroundColor = 'transparent';
                buttonSpan.style.color = primaryColor;
                buttonSpan.style.borderColor = primaryColor;
                buttonSpan.style.boxShadow = 'none';
            }
        });
    }


    // Show/hide custom amount field
    function toggleCustomField() {
        if (customRadio.checked) {
            customField.style.display = 'block';
            customInput.setAttribute('required', 'required');
            customInput.focus();
        } else {
            customField.style.display = 'none';
            customInput.removeAttribute('required');
            customInput.name = 'custom_amount';
            customInput.value = '';
        }
    }


    // Event listeners
    rechargeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            updateSelectedVisuals();
            toggleCustomField();
        });
    });

    // Apply initial visual state on page load
    updateSelectedVisuals();
    toggleCustomField();
});
