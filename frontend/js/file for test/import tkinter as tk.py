import tkinter as tk
from tkinterhtml import HtmlFrame
import mysql.connector

class MessageManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Management App")
        self.create_database_connection()
        self.create_ui()

    def create_database_connection(self):
        try:
            # Replace with your actual database credentials
            self.conn = mysql.connector.connect(
                user='ghostbin3',
                password='Ahmed197524',
                host='ghostbin3.mysql.pythonanywhere-services.com',
                port=3306,
                database='ghostbin3$bakersbox'
            )

            if self.conn.is_connected():
                print("Connected to MySQL server")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_ui(self):
        self.html_frame = HtmlFrame(self.root, horizontal_scrollbar="auto")
        self.html_frame.grid(row=0, column=0, sticky="nsew")

        self.html_frame.set_content('''
            <!DOCTYPE html>
            <html lang="es">
            <head>
              <meta charset="UTF-8">
              <title>Tabla de Mensajes</title>
              <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>

                <div class="container mt-4">
                    <h1>Tabla de Mensajes</h1>
                    <button id="btnTraerMensajes" class="btn btn-primary mb-3">Traer Mensajes</button>
                    <table id="tablaMensajes" class="table">
                      <thead class="thead-dark">
                        <tr>
                          <th scope="col">id</th>  
                          <th scope="col">nombre</th>
                          <th scope="col">celular</th>
                          <th scope="col">email</th>
                          <th scope="col">mensaje</th>
                          <th scope="col">fecha envío</th>
                          <th scope="col">leído</th>
                          <th scope="col">gestion</th>
                          <th scope="col">fecha gestion</th>
                        </tr>
                      </thead>
                      <tbody>
                        <!-- Dynamic rows will be inserted here -->
                      </tbody>
                    </table>
                  </div>

                  <div class="container mt-4">
                    <h1>Formulario de Gestión</h1>
                    <form id="formcontect">
                      <div class="form-group">
                        <label for="idInput">ID</label>
                        <input type="text" class="form-control" id="idInput" placeholder="Ingrese el ID">
                      </div>
                      <div class="form-group">
                        <label for="detalleInput">Detalle de la Gestión</label>
                        <textarea class="form-control" id="detalleInput" rows="4" placeholder="Ingrese el detalle de la gestión"></textarea>
                      </div>
                      <button type="submit" class="btn btn-primary">Enviar</button>
                    </form>
                  </div>

                <script>
                    ${self.get_javascript_code()}
                </script>

            </body>
            </html>
        ''')

    def get_javascript_code(self):
        return '''
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
        '''

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageManagementApp(root)
    root.mainloop()
