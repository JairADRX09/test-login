document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    fetch('http://localhost:3000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        document.getElementById('message').textContent = data.message;
      } else {
        document.getElementById('message').textContent = 'Login exitoso';
      }
    })
    .catch(error => {
      document.getElementById('message').textContent = 'Error en el login';
    });
  });
  