document.addEventListener('DOMContentLoaded', function () {
    const errorMessages = document.querySelectorAll('.error-message');

    errorMessages.forEach(errorMessage => {
        if (errorMessage.textContent.trim() !== '') {
            const inputField = errorMessage.previousElementSibling;

            if (inputField) {
                inputField.classList.add('error');
                console.log(`Added error class to: ${inputField.name}`); // Debugging log
            } else {
                console.log("No input field found for error message!");
            }
        }
    });
});
