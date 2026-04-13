document.addEventListener('DOMContentLoaded', async () => {
  //get current use
  const res = await fetch('/api/me', {
    credentials: 'include'
  });
  //if we did not get a user they are not logged in, redirect to login
  if (!res.ok) {
    window.location.href = '/';
    return;
  }
  //if we are good get user data
  const user = await res.json();
  //username
  const fullName = user.username || user.email;
  document.getElementById('welcome').textContent =
    'Hello ' + fullName + ', you have logged in';
  //no reset button if github user
  if (user.type === "github") {
    document.getElementById('resetBtn').style.display = "none";
  }
  //setup the logout button
  document.getElementById('logoutBtn').addEventListener('click', async () => {
    await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
    });
    window.location.href = '/';
  });
  //setup reset button if is still there
  document.getElementById('resetBtn').addEventListener('click', () => {
    window.location.href = '/reset';
  });

});
