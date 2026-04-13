document.addEventListener('DOMContentLoaded', async () => {
  // Get current user (checks existing session via cookies)
  const res = await fetch('/api/me', {
    credentials: 'include'
  });

  // If no valid user, redirect to login/home page
  if (!res.ok) {
    window.location.href = '/';
    return;
  }

  // Parse user data from response
  const user = await res.json();

  // Use username if available, otherwise fall back to email
  const fullName = user.username || user.email;

  // Show welcome message in UI
  document.getElementById('welcome').textContent =
    'Hello ' + fullName + ', you have logged in';

  // Hide reset button for GitHub users (no password to reset)
  if (user.type === "github") {
    document.getElementById('resetBtn').style.display = "none";
  }

  // Log out user: clear session on server, then redirect
  document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
    });
    window.location.href = '/';
  });

  // Navigate to reset page (only relevant for non-GitHub users)
  document.getElementById('resetBtn').addEventListener('click', () => {
    window.location.href = '/reset';
  });

});
