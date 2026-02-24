document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('loginForm');
    const githubBtn = document.getElementById('githubLoginBtn');

    // Standard login submit
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('/api/login_standard', {   // ✅ changed endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/home';
            } else {
                alert('Login failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during login.');
        });
    });

    // GitHub OAuth login redirect
    if (githubBtn) {
        githubBtn.addEventListener('click', function () {
            window.location.href = '/api/login_github';  // ✅ changed endpoint
        });
    }

});
