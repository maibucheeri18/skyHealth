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
            submitForm(firstName.value, lastName.value, email.value, username.value, password.value);
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

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function submitForm(fName, lName, email, un, ps) {
        // Here you would normally collect the form data and send to the backend
        const formData = new FormData(form);
        
        console.log(formData)
        
        // For demonstration purposes - showing the data that would be sent
        var data = {}
        console.log('Form data to be submitted:');
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
            data[key] = value
        }
        
        fetch('/account/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body:  JSON.stringify({
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'username': data['username'],
                'password': data['password']
            })
        })
        
        // Return to read-only state
        disableEditMode();

    }
})
