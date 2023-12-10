document.getElementById('btnTraerMensajes').addEventListener('click', () => {
  fetch('https://ghostbin3.pythonanywhere.com/mensajes')
      .then(response => response.json())
      .then(datos => {
          console.log("datos", datos);
          const tablaBody = document.querySelector('#tablaMensajes tbody');
          tablaBody.innerHTML = ''; // Limpiar tabla antes de agregar nuevos datos

          // Iterar sobre los datos y agregar filas a la tabla
          datos.forEach(dato => {
              const fila = document.createElement('tr');
              fila.innerHTML = `
                  <td>${dato.id}</td>
                  <td>${dato.nombre}</td>
                  <td>${dato.celular}</td>
                  <td>${dato.email}</td>
                  <td>${dato.mensaje}</td>
                  <td>${dato.fecha_envio}</td>
                  <td>${dato.leido}</td>
                  <td>${dato.gestion}</td>
                  <td>${dato.fecha_gestion}</td>
              `;
              tablaBody.appendChild(fila);
          });
      })
      .catch(error => {
          console.error('Error al obtener los datos:', error);
      });
});

document.getElementById('formcontect').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent default form submission

  // Obtener los valores de los campos
  const id = document.getElementById('idInput').value;
  const gestion = document.getElementById('detalleInput').value;

  const formData = new FormData();
  formData.append('gestion', gestion); // Add the detail to the form data

  fetch(`https://ghostbin3.pythonanywhere.com/mensajes/${id}`, {
      method: 'PUT',
      body: formData
  })
      .then(response => response.json())
      .then(data => {
          console.log('Respuesta del servidor:', data);
          // You can show a confirmation to the user or handle the server response here
      })
      .catch(error => {
          console.error('Error al enviar los datos:', error);
      });
});