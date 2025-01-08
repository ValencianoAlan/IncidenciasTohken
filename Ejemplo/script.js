// Agrega un listener al formulario para capturar el evento de envío
document.getElementById('loginForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Previene que el formulario recargue la página

  // Obtiene los valores ingresados en el formulario
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    // Envía los datos al backend mediante una solicitud POST
    const response = await fetch('http://localhost:3000/login', {
      method: 'POST', // Tipo de solicitud
      headers: { 'Content-Type': 'application/json' }, // Indica que se envían datos en formato JSON
      body: JSON.stringify({ username, password }), // Convierte los datos a JSON
    });

    const result = await response.json(); // Convierte la respuesta del servidor en un objeto JavaScript

    if (response.ok) { // Si la respuesta es exitosa
      alert(result.message); // Muestra un mensaje de éxito
    } else {
      const errorMessage = document.getElementById('errorMessage'); // Selecciona el elemento para mensajes de error
      errorMessage.textContent = result.message; // Muestra el mensaje de error del servidor
      errorMessage.style.display = 'block'; // Hace visible el mensaje de error
    }
  } catch (err) {
    console.error('Error:', err); // Muestra cualquier error de red o del servidor en la consola
    alert('Error al conectar con el servidor'); // Muestra un mensaje de error al usuario
  }
});
