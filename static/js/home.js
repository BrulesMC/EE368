document.addEventListener('DOMContentLoaded', () => {
  // Fetch current user info
  fetch('/api/me')
    .then(response => {
      if (!response.ok) {
        window.location.href = '/'; // not logged in
        return;
      }
      return response.json();
    })
    .then(user => {
      if (!user) return;

<<<<<<< Updated upstream
      const fullName = `${user.first_name} ${user.last_name}`;
      document.getElementById('welcome').textContent =
        'Hello ' + fullName + ', you have logged in';
    })
    .catch(() => {
      window.location.href = '/';
=======
  if (!res.ok) {
    window.location.href = '/'; // not logged in
    return;
  }

  const user = await res.json();

  // Display welcome message
  const fullName = user.first_name && user.last_name
    ? `${user.first_name} ${user.last_name}`
    : user.email;

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
>>>>>>> Stashed changes
    });

  // Logout button
  document.getElementById('logoutBtn').addEventListener('click', () => {
    fetch('/api/logout', { method: 'POST' })
      .then(() => window.location.href = '/');
  });

  // Reset password button
  document.getElementById('resetBtn').addEventListener('click', () => {
    window.location.href = '/reset';
  });
});
