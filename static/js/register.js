document.addEventListener('DOMContentLoaded', () => {

    // Get the registration form from the page
    const form = document.getElementById('registerForm');

    // Handle form submission for creating a new account
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload

        // Collect user input from form fields
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Send registration request to server
        const res = await fetch('/api/register', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        // Parse server response
        const data = await res.json();

        // If registration succeeds, redirect to home (user is likely logged in)
        if (data.success) {
            window.location.href = '/home';
        } else {
            // Show error message if registration fails
            alert(data.error || 'Registration failed');
        }
    });

});
