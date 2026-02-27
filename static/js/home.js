document.addEventListener('DOMContentLoaded', async () => {

  // Fetch current user info
  const res = await fetch('/api/me', {
    credentials: 'include'
  });

  if (!res.ok) {
    window.location.href = '/'; // not logged in
    return;
  }

  const user = await res.json();

  // Display welcome message
  const fullName = user.first_name && user.last_name
    ? `${user.first_name} ${user.last_name}`
    : user.username;

  document.getElementById('welcome').textContent =
    'Hello ' + fullName + ', you have logged in';

  // Hide reset password for GitHub users
  if (user.type === "github") {
    document.getElementById('resetBtn').style.display = "none";
  }

  // Logout button
  document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
    });

    window.location.href = '/';
  });

  // Reset password button
  document.getElementById('resetBtn').addEventListener('click', () => {
    window.location.href = '/reset';
  });

});