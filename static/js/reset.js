document.addEventListener('DOMContentLoaded', () => {
  const resetForm = document.getElementById('resetForm');
  const backHomeBtn = document.getElementById('backHomeBtn');

  resetForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    try {
      const response = await fetch('/api/change-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: newPassword })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.message || "Error changing password");
        return;
      }

      alert("Password changed successfully! You will be logged out.");

      // Auto logout
      await fetch('/api/logout', { method: 'POST' });
      window.location.href = '/';
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }
  });

  backHomeBtn.addEventListener('click', () => {
    window.location.href = '/home';
  });
});
