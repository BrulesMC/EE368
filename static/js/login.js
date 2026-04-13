document.addEventListener('DOMContentLoaded', function () {

    // Get form and GitHub login button from the page
    const form = document.getElementById('loginForm');
    const githubBtn = document.getElementById('githubLoginBtn');

    // Create and attach a hidden error message element for login feedback
    const errorMsg = document.createElement('p');
    errorMsg.style.color = 'red';
    errorMsg.style.display = 'none';
    form.appendChild(errorMsg);
    
    // Handle standard email/password login submission
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent page reload

        // Get user input from form fields
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Send login request to server
        fetch('/api/login_standard', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            // If login successful, redirect to home page
            if (data.success) {
                window.location.href = '/home';
            } else {
                // Show error message and reset password field for retry
                errorMsg.textContent = 'Login failed: ' + (data.error || 'Incorrect email or password');
                errorMsg.style.display = 'block';
                document.getElementById('password').value = '';
                document.getElementById('password').focus();
            }
        })
        .catch(error => {
            // Handle network/server errors
            console.error('Error:', error);
            errorMsg.textContent = 'An error occurred during login.';
            errorMsg.style.display = 'block';
        });
    });

    // Redirect user to GitHub OAuth flow when button is clicked
    if (githubBtn) {
        githubBtn.addEventListener('click', function () {
            window.location.href = '/api/login_github';
        });
    }

});
