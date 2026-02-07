document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('resetForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const email = document.getElementById('email').value;

        fetch('/api/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('If this email exists, a reset link has been sent.');
                window.location.href = '/';
            } else {
                alert(data.message || 'Unable to process request.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
