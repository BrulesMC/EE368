document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('resetForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const new_password = document.getElementById('new_password').value;

        const res = await fetch('/api/reset_password', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_password })
        });

        const data = await res.json();

        if (data.success) {
            alert("Password updated!");
            window.location.href = '/home';
        } else {
            alert(data.error || "Error updating password");
        }
    });

});