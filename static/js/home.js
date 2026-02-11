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

      const fullName = `${user.first_name} ${user.last_name}`;
      document.getElementById('welcome').textContent =
        'Hello ' + fullName + ', you have logged in';
    })
    .catch(() => {
      window.location.href = '/';
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
