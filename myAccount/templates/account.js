document.addEventListener('DOMContentLoaded', function() {
    const actionButton = document.getElementById('action-button');
    const formOuterContainer = document.getElementById('form-outer-container');
    const formInputs = document.querySelectorAll('#user-form input');
    const form = document.getElementById('user-form');
    let isEditing = false;

    const takenUsernames = ['takenuser1', 'takenuser2', 'takenuser3', 'admin', 'user'];

    actionButton.addEventListener('click', function() {
        if (isEditing) {
            validateAndSubmit();
        } else {
            enableEditMode();
        }
    });

    function enableEditMode() {
        isEditing = true;
        actionButton.textContent = 'Save';
        formOuterContainer.classList.add('edit-mode');

        document.querySelectorAll('.invalid-feedback').forEach(elem => elem.textContent = '');
        document.querySelectorAll('.is-invalid').forEach(input => input.classList.remove('is-invalid'));

        formInputs.forEach(input => {
            if (input.id !== 'password') {
                input.readOnly = false;
                input.classList.remove('bg-light');
            }
            if (input.id === 'password') {
                input.readOnly = false;
                input.classList.remove('bg-light');
                input.value = '';
                input.placeholder = 'Enter new password';
            }
        });
    }

    function disableEditMode() {
        isEditing = false;
        actionButton.textContent = 'Edit';
        formOuterContainer.classList.remove('edit-mode');

        formInputs.forEach(input => {
            input.readOnly = true;
            input.classList.add('bg-light');
            input.classList.remove('is-invalid');

            if (input.id === 'password') {
                input.value = '••••••••••••';
                input.placeholder = '';
            }
        });

        document.querySelectorAll('.invalid-feedback').forEach(elem => elem.textContent = '');
    }

    function validateAndSubmit() {
        let isValid = true;

        document.querySelectorAll('.invalid-feedback').forEach(elem => elem.textContent = '');
        document.querySelectorAll('.is-invalid').forEach(input => input.classList.remove('is-invalid'));

        const firstName = document.getElementById('first_name');
        if (!firstName.value.trim()) {
            showError(firstName, 'First name is required');
            isValid = false;
        }

        const lastName = document.getElementById('last_name');
        if (!lastName.value.trim()) {
            showError(lastName, 'Last name is required');
            isValid = false;
        }

        const email = document.getElementById('email');
        if (!email.value.trim()) {
            showError(email, 'Email is required');
            isValid = false;
        } else if (!isValidEmail(email.value)) {
            showError(email, 'Incorrect email format');
            isValid = false;
        }

        const username = document.getElementById('username');
        if (!username.value.trim()) {
            showError(username, 'Username is required');
            isValid = false;
        } else if (takenUsernames.includes(username.value.trim().toLowerCase())) {
            showError(username, 'Username already taken');
            isValid = false;
        }

        const password = document.getElementById('password');
        if (password.value.trim() !== '' && password.value !== '••••••••••••') {
            if (!isValidPassword(password.value)) {
                showError(password, 'Password must have at least 8 characters, 1 uppercase, 1 lowercase, 1 number, and 1 special character');
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
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return passwordRegex.test(password);
    }

    function submitForm() {
        const formData = new FormData(form);

        console.log('Form data to submit:');
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        alert('Profile updated successfully!');
        disableEditMode();
    }
});
