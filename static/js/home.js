document.addEventListener('DOMContentLoaded', async () => {

  const res = await fetch('/api/me', {
    credentials: 'include'
  });

  if (!res.ok) {
    window.location.href = '/';
    return;
  }

  const user = await res.json();

  const fullName = user.username || user.email;
  document.getElementById('welcome').textContent =
    'Hello ' + fullName + ', you have logged in';

  if (user.type === "github") {
    document.getElementById('resetBtn').style.display = "none";
  }

  document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
    });
    window.location.href = '/';
  });

  document.getElementById('resetBtn').addEventListener('click', () => {
    window.location.href = '/reset';
  });

});