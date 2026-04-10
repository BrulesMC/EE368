document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('loginForm');
    const githubBtn = document.getElementById('githubLoginBtn');

    const errorMsg = document.createElement('p');
    errorMsg.style.color = 'red';
    errorMsg.style.display = 'none';
    form.appendChild(errorMsg);
    
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
               errorMsg.textContent = 'Login failed: ' + (data.error || 'Incorrect email or password');
                errorMsg.style.display = 'block';
                document.getElementById('password').walue = '';
                document.getElementById('password').focus();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMsg.textContent = 'An error occurred during login.';
            error.Msg.style.display = 'block';
        });
    });

    // GitHub OAuth login redirect
    if (githubBtn) {
        githubBtn.addEventListener('click', function () {
            window.location.href = '/api/login_github';
        });
    }

});
