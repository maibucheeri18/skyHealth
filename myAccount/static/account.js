document.addEventListener('DOMContentLoaded', function() {
    const actionButton = document.getElementById('action-button');
    const formOuterContainer = document.getElementById('form-outer-container');
    const formInputs = document.querySelectorAll('#user-form input');
    const form = document.getElementById('user-form');
    let isEditing = false;
    
    // List of taken usernames (for simulation purposes)
    const takenUsernames = ['takenuser1', 'takenuser2', 'takenuser3', 'admin', 'user'];

    // Handle button click (either to edit or to save)
    actionButton.addEventListener('click', function() {
        if (isEditing) {
            // Submit the form with validation
            validateAndSubmit();
        } else {
            // Enable editing mode
            enableEditMode();
        }
    });

    function enableEditMode() {
        isEditing = true;
        actionButton.textContent = 'Save';
        
        // Add blue border to the outer container when in edit mode
        formOuterContainer.classList.add('edit-mode');
        
        // Clear any previous error messages
        document.querySelectorAll('.invalid-feedback').forEach(elem => {
            elem.textContent = '';
        });
        
        // Remove error styling from inputs
        document.querySelectorAll('.is-invalid').forEach(input => {
            input.classList.remove('is-invalid');
        });
        
        formInputs.forEach(input => {
            if (input.id !== 'password') { // Don't make password editable in this simple example
                input.readOnly = false;
                input.classList.remove('bg-light');
            }
            
            // For demo purposes, also make password editable
            if (input.id === 'password') {
                input.readOnly = false;
                input.classList.remove('bg-light');
                input.value = ''; // Clear password field for security
                input.placeholder = 'Enter new password';
            }
        });
    }

    function disableEditMode() {
        isEditing = false;
        actionButton.textContent = 'Edit';
        
        // Remove blue border when returning to view mode
        formOuterContainer.classList.remove('edit-mode');
        
        formInputs.forEach(input => {
            input.readOnly = true;
            input.classList.add('bg-light');
            
            // Remove any validation styling
            input.classList.remove('is-invalid');
            
            // Reset password field to dots
            if (input.id === 'password') {
                input.value = '••••••••••••';
                input.placeholder = '';
            }
        });
        
        // Clear error messages
        document.querySelectorAll('.invalid-feedback').forEach(elem => {
            elem.textContent = '';
        });
    }
    
    function validateAndSubmit() {
        let isValid = true;
        
        // Clear all previous error messages
        document.querySelectorAll('.invalid-feedback').forEach(elem => {
            elem.textContent = '';
        });
        document.querySelectorAll('.is-invalid').forEach(input => {
            input.classList.remove('is-invalid');
        });
        
        // Validate first name (required)
        const firstName = document.getElementById('first_name');
        if (!firstName.value.trim()) {
            showError(firstName, 'First name is required');
            isValid = false;
        }
        
        // Validate last name (required)
        const lastName = document.getElementById('last_name');
        if (!lastName.value.trim()) {
            showError(lastName, 'Last name is required');
            isValid = false;
        }
        
        // Validate email (required and format)
        const email = document.getElementById('email');
        if (!email.value.trim()) {
            showError(email, 'Email is required');
            isValid = false;
        } else if (!isValidEmail(email.value)) {
            showError(email, 'Incorrect email. Please ensure your email is in the correct format (name@sky.com)');
            isValid = false;
        }
        
        // Validate username (required and unique)
        const username = document.getElementById('username');
        if (!username.value.trim()) {
            showError(username, 'Username is required');
            isValid = false;
        } else if (takenUsernames.includes(username.value.trim().toLowerCase())) {
            // Check if username is already taken
            showError(username, 'The username has already been taken. Please choose a different one.');
            isValid = false;
        }
        
        // Validate password (if changed)
        const password = document.getElementById('password');
        if (password.value.trim() !== '' && password.value !== '••••••••••••') {
            if (!isValidPassword(password.value)) {
                showError(password, 'Incorrect password. It must have at least 8 characters that include at least 1 lowercase characters, 1 uppercase characters, 1 number and 1 special character');
                isValid = false;
            }
        }
        
        if (isValid) {
            submitForm();
        }
    }
    
    function showError(inputElement, message) {
        inputElement.classList.add('is-invalid');
        const errorElement = document.getElementById(inputElement.id + '_error');
        errorElement.textContent = message;
    }
    
    function isValidEmail(email) {
        // This regex pattern checks for format similar to name@sky.com
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function isValidPassword(password) {
        // Password must have at least 8 characters with 1 lowercase, 1 uppercase, 1 number, and 1 special character
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return passwordRegex.test(password);
    }

    function submitForm() {
        // Here you would normally collect the form data and send to the backend
        const formData = new FormData(form);
        
        // For demonstration purposes - showing the data that would be sent
        console.log('Form data to be submitted:');
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
        
        // This is where you would add the AJAX call to your backend
        // For now, just simulate a successful update
        alert('Profile updated successfully!');
        
        // Return to read-only state
        disableEditMode();

    // This should be added to your existing JavaScript for form submission
function submitForm() {
const formData = new FormData();

// Get values and append them with the correct field names
formData.append('first_name', document.getElementById('first_name').value);
formData.append('last_name', document.getElementById('last_name').value);
formData.append('email', document.getElementById('email').value);
formData.append('username', document.getElementById('username').value);
formData.append('password', document.getElementById('password').value);

// Add CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
formData.append('csrfmiddlewaretoken', csrfToken);

// Send AJAX request
fetch('/account/', {  // Adjust the URL to match your route
method: 'POST',
body: formData,
headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrfToken
}
})
.then(response => response.json())
.then(data => {
if (data.success) {
    alert('Profile updated successfully!');
    disableEditMode();
} else {
    // Handle validation errors from server
    if (data.errors) {
        Object.keys(data.errors).forEach(field => {
            const input = document.getElementById(field);
            const errorElement = document.getElementById(field + '_error');
            if (input && errorElement) {
                input.classList.add('is-invalid');
                errorElement.textContent = data.errors[field];
            }
        });
    }
}
})
.catch(error => {
console.error('Error:', error);
alert('An error occurred while updating your profile.');
});
}
    }
});
