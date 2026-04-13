document.addEventListener('DOMContentLoaded', () => {

    // Get the password reset form from the page
    const form = document.getElementById('resetForm');

    // Handle form submission for updating password
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload

        // Get new password input from user
        const new_password = document.getElementById('new_password').value;

        // Send password update request to server
        const res = await fetch('/api/reset_password', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_password })
        });

        // Parse server response
        const data = await res.json();

        // If update succeeds, notify user and redirect to home
        if (data.success) {
            alert("Password updated!");
            window.location.href = '/home';
        } else {
            // Show error if password update fails
            alert(data.error || "Error updating password");
        }
    });

});
