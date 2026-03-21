document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const adminLoginForm = document.getElementById('admin-login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      try {
        const data = await login(email, password);
        if (data && data.token) {
          localStorage.setItem('token', data.token);
          localStorage.setItem('user', JSON.stringify(data.user));
          window.location.href = '/frontend/user/dashboard.html';
        }
      } catch(err) {
        alert('Login failed: ' + err.message);
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const full_name = document.getElementById('full_name').value;
      
      try {
        const data = await register(email, username, password, full_name);
        if (data && data.token) {
          localStorage.setItem('token', data.token);
          localStorage.setItem('user', JSON.stringify(data.user));
          window.location.href = '/frontend/user/dashboard.html';
        }
      } catch(err) {
        alert('Registration failed: ' + err.message);
      }
    });
  }

  if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email = document.getElementById('admin-email').value;
      const password = document.getElementById('admin-password').value;
      
      try {
        const data = await adminLogin(email, password);
        if (data && data.token) {
          localStorage.setItem('token', data.token);
          localStorage.setItem('user', JSON.stringify(data.user));
          if (data.user.is_admin) {
            window.location.href = '/frontend/admin/dashboard.html';
          } else {
            alert('Not an admin account');
          }
        }
      } catch(err) {
        alert('Admin login failed: ' + err.message);
      }
    });
  }
});
