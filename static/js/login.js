document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('loginForm');
    const githubBtn = document.getElementById('githubLoginBtn');

    // Standard login submit
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

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
            if (data.success) {
                window.location.href = '/home';
            } else {
                alert('Login failed: ' + (data.error || 'Unknown error'));
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
            window.location.href = '/api/login_github';
        });
    }

});
