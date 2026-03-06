/**
 * Formats the time difference in Days, Hours, Minutes, and Seconds
 * @param {number} distance - time difference in milliseconds
 * @returns {string} formatted string "Xd Xh Xm Xs"
 */
function formatTime(distance) {
    const MS_IN_SECOND = 1000;
    const MS_IN_MINUTE = 60 * MS_IN_SECOND;
    const MS_IN_HOUR = 60 * MS_IN_MINUTE;
    const MS_IN_DAY = 24 * MS_IN_HOUR;

    // Ensure the distance is not negative
    if (distance < 0) {
        distance = 0;
    }

    const days = Math.floor(distance / MS_IN_DAY);
    const hours = Math.floor((distance % MS_IN_DAY) / MS_IN_HOUR);
    const minutes = Math.floor((distance % MS_IN_HOUR) / MS_IN_MINUTE);
    const seconds = Math.floor((distance % MS_IN_MINUTE) / MS_IN_SECOND);

    return `${days}d ${hours}h ${minutes}m ${seconds}s`;
}

/**
 * Starts the countdown for a specific element
 * @param {HTMLElement} timerElement - element with data-start-date and data-end-date
 */
function startCountdown(timerElement) {
    const outputSpan = timerElement.querySelector('span');
    const startDateAttr = timerElement.getAttribute('data-start-date');
    const endDateAttr = timerElement.getAttribute('data-end-date');
    
    // Helper functions to get timestamp
    // Uses new Date(string).getTime() to get milliseconds
    const parseDate = (dateString) => new Date(dateString).getTime();

    const startTime = startDateAttr ? parseDate(startDateAttr) : 0;
    const endTime = endDateAttr ? parseDate(endDateAttr) : 0;

    let targetDate;
    let type; // 'start' (countdown to start) or 'end' (countdown to end)
    
    // Prevent issues if dates cannot be parsed (resulting in NaN)
    if (isNaN(startTime) || isNaN(endTime)) {
        outputSpan.textContent = "Invalid Date!";
        timerElement.style.color = 'gray';
        return;
    }

    const now = new Date().getTime();

    if (now < startTime) {
        // Auction has not started yet (countdown to start)
        targetDate = startTime;
        type = 'start';
        timerElement.innerHTML = `Começa em: <span>${formatTime(targetDate - now)}</span>`;
    } else if (now >= startTime && now < endTime) {
        // Auction active (countdown to end)
        targetDate = endTime;
        type = 'end';
        timerElement.innerHTML = `Termina em: <span>${formatTime(targetDate - now)}</span>`;
    } else {
        // Auction ended

        return;
    }

    const interval = setInterval(() => {
        const now = new Date().getTime();
        let distance = targetDate - now;

        if (distance <= 0) {
            if (type === 'start') {
                // Auction started, now count down to the end
                targetDate = endTime;
                type = 'end';
                // Recalculate distance and update parent element text
                distance = targetDate - now;
                
                // Change text to 'Ends in'
                timerElement.innerHTML = `Termina em: <span>${formatTime(distance)}</span>`;
                // Update reference to the span
                const currentOutputSpan = timerElement.querySelector('span');
                currentOutputSpan.textContent = formatTime(distance);
                
                // If distance is still <= 0 after transition, end immediately
                if (distance <= 0) {
                    clearInterval(interval);
                    timerElement.innerHTML = `<span style="color: red;">Finalizado!</span>`;
                }
            } else {
                // Auction ended
                clearInterval(interval);
                timerElement.innerHTML = `<span style="color: red;">Finalizado!</span>`;
            }
        } else {
            // If countdown is still active, just update the span
            timerElement.querySelector('span').textContent = formatTime(distance);
        }
    }, 1000);
}

// Initialize all timers when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const timers = document.querySelectorAll('.countdown-timer');
    timers.forEach(timer => startCountdown(timer));
});
