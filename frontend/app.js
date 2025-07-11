// URL de tu backend en Render
const API_URL = 'https://prueba-flask.onrender.com/api/mensaje';

fetch(API_URL)
    .then(response => response.json())
    .then(data => {
        document.getElementById('titulo').textContent = data.mensaje;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('titulo').textContent = 'Experimento con Flask';
    });