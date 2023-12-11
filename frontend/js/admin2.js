document.getElementById('btnTraerMensajes').addEventListener('click', () => {
    fetch(`https://ghostbin4.pythonanywhere.com/mensajes`)
      .then(response => response.json())
      .then(datos => {
        console.log("datos", datos)
        const tablaBody = document.querySelector('#tablaMensajes tbody');
        tablaBody.innerHTML = ''; // Limpiar tabla antes de agregar nuevos datos

        // Iterar sobre los datos y agregar filas a la tabla
        datos.forEach(dato => {
          const fila = document.createElement('tr');
          fila.innerHTML = `
            <td>${dato.id}</td>
            <td>${dato.nombre}</td>
            <td>${dato.celular}</td>
            <td>${dato.mensaje}</td>
            <td>${dato.fecha_envio}</td>
            <td>${dato.mensaje}</td>
            <td>${dato.leido}</td>
          `;
          tablaBody.appendChild(fila);
        });
      })
      .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
});

document.getElementById('formularioContacto').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Get the values from the fields
    const id = document.getElementById('idInput').value;
    const gestion = document.getElementById('detalleInput').value;

    console.log('Submitting data:', { id, gestion });

    const formData = new FormData();
    formData.append('gestion', gestion);

    fetch(`https://ghostbin4.pythonanywhere.com/mensajes/${id}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        // Add any additional handling as needed
    })
    .catch(error => {
        console.error('Error sending data:', error);
    });
});
