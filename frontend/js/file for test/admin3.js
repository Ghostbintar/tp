document.getElementById('btnTraerMensajes').addEventListener('click', () => {
    console.log("Fetching messages...");
    fetch('https://ghostbin3.pythonanywhere.com/mensajes')
        .then(response => response.json())
        .then(datos => {
            console.log("Received data:", datos);
            const tablaBody = document.querySelector('#tablaMensajes tbody');
            tablaBody.innerHTML = '';

            datos.forEach(dato => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${dato.id}</td>
                    <td>${dato.nombre}</td>
                    <td>${dato.celular}</td>
                    <!-- Add more table cells as needed -->
                `;
                tablaBody.appendChild(fila);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});

document.getElementById('formcontect').addEventListener('submit', function (event) {
    event.preventDefault();

    const id = document.getElementById('idInput').value;
    const gestion = document.getElementById('detalleInput').value;

    console.log("Submitting form with id:", id, "and gestion:", gestion);

    const formData = new FormData();
    formData.append('gestion', gestion);

    fetch(`https://ghostbin3.pythonanywhere.com/mensajes/${id}`, {
        method: 'PUT',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            // Consider updating the UI or providing user feedback based on the server response
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
});
