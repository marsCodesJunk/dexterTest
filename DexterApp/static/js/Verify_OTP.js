// Get references to elements
const otpBoxes = document.querySelectorAll('.otp-box'); // OTP Input Boxes
const otpForm = document.querySelector('form'); // OTP Form

// Handle OTP input focus movement
otpBoxes.forEach((box, index) => {
    box.addEventListener('input', (e) => {
        const value = e.target.value;
        if (value.length === 1 && index < otpBoxes.length - 1) {
            otpBoxes[index + 1].focus();
        }
    });

    box.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && index > 0 && !e.target.value) {
            otpBoxes[index - 1].focus();
        }
    });
});

// Handle OTP form submission
otpForm.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent form submission

    // Collect OTP
    const otp = Array.from(otpBoxes).map(box => box.value).join('');

    if (otp.length === 5) {
        otpForm.submit(); // Submit the form if OTP is valid
    } else {
        alert('Please enter a valid 5-digit OTP.');
    }
});

