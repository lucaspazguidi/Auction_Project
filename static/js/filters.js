document.addEventListener('DOMContentLoaded', () => {

    // Select all clickable badge elements
    const badges = document.querySelectorAll('.badge.selectable');

    // Update visual state based on selection
    // Adds or removes the "selected" class
    function updateSelected() {
        badges.forEach(badge => {
            const input = badge.querySelector('input');
            // Applies "selected" when the corresponding input is checked
            badge.classList.toggle('selected', input.checked);
        });
    }

    // Attach click listener to each badge
    // Ensures clicking the badge selects its radio/checkbox
    badges.forEach(badge => {
        badge.addEventListener('click', () => {
            const input = badge.querySelector('input');

            input.checked = true; // forces selection

            updateSelected(); // refresh UI
        });
    });

    // Initial update on page load
    updateSelected();
});
