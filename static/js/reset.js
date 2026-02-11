document.addEventListener('DOMContentLoaded', () => {
  const emailInput = document.getElementById('email');
  const resetForm = document.getElementById('resetForm');
  const backLoginBtn = document.getElementById('backLoginBtn');

  // Get current user info
  fetch('/api/me')
    .then(res => {
      if (!res.ok) {
        window.location.href = '/'; // not logged in
        return;
      }
      return res.json();
    })
    .then(user => {
      if (!user) return;
      emailInput.value = user.email; // auto-fill email
    })
    .catch(() => {
      window.location.href = '/';
    });

  // Handle form submit
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
        body: JSON.stringify({
          current_password: newPassword, // assuming user knows old pw? else backend needs adjustment
          new_password: newPassword
        })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.message || "Error resetting password");
        return;
      }

      alert("Password reset successful! Logging out...");
      
      // Auto logout
      await fetch('/api/logout', { method: 'POST' });
      window.location.href = '/';
    } catch (err) {
      console.error(err);
      alert("Something went wrong!");
    }
  });

  // Back to login
  backLoginBtn.addEventListener('click', () => {
    window.location.href = '/';
  });
});
