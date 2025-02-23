const signupBtn = document.querySelector('.submit-btn'); // Sign-Up Button
const popup = document.getElementById('popup'); // Popup Container
function editField(fieldId) {
    const field = document.getElementById(fieldId);
    if (field.readOnly) {
      field.readOnly = false;
      field.focus();
    } else {
      field.readOnly = true;
      // Save changes (e.g., via API call)
      console.log(`${fieldId} updated:`, field.value);
    }
  }

  function updatePassword() {
    alert("Redirecting to password update page...");
    // Redirect or open a modal for password update
    window.location.href = "/update-password";
  }

  function confirmDelete() {
    const confirmation = confirm("Are you sure you want to delete your account?");
    window.location.href = "{% url 'home' %}";
  }
