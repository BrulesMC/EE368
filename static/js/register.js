document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('user_name').value;
        const password = document.getElementById('password').value;

        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Registration successful! Please log in.');
                window.location.href = '/';
            } else {
                alert('Registration failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during registration.');
        });
    });
});
