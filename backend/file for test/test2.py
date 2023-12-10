# Importa las bibliotecas necesarias
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class MensajeApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Aplicación de Mensajes")
        
        # Variables de la interfaz
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()

        # Crear los elementos de la interfaz
        tk.Label(master, text="ID:").grid(row=0, column=0, sticky=tk.E)
        tk.Entry(master, textvariable=self.id_var).grid(row=0, column=1)
        tk.Button(master, text="Mostrar Todos", command=self.mostrar_todos).grid(row=0, column=2)
        
        tk.Label(master, text="Nombre:").grid(row=1, column=0, sticky=tk.E)
        tk.Label(master, text="Celular:").grid(row=2, column=0, sticky=tk.E)
        tk.Label(master, text="Email:").grid(row=3, column=0, sticky=tk.E)
        tk.Label(master, text="Mensaje:").grid(row=4, column=0, sticky=tk.E)

        tk.Entry(master, textvariable=self.nombre_var).grid(row=1, column=1)
        tk.Entry(master, textvariable=self.celular_var).grid(row=2, column=1)
        tk.Entry(master, textvariable=self.email_var).grid(row=3, column=1)
        tk.Entry(master, textvariable=self.mensaje_var).grid(row=4, column=1)
        tk.Button(master, text="Enviar Mensaje", command=self.enviar_mensaje).grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(master, text="Mostrar por ID", command=self.mostrar_por_id).grid(row=6, column=0, columnspan=2)
        tk.Button(master, text="Eliminar Mensaje", command=self.eliminar_mensaje).grid(row=7, column=0, columnspan=2)
        tk.Button(master, text="Responder Mensaje", command=self.responder_mensaje).grid(row=8, column=0, columnspan=2, pady=10)

    def conectar_base_datos(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bakers_box"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error de conexión a la base de datos: {err}")
            self.master.destroy()

    def enviar_mensaje(self):
        self.conectar_base_datos()

        nombre = self.nombre_var.get()
        celular = self.celular_var.get()
        email = self.email_var.get()
        mensaje = self.mensaje_var.get()

        sql = "INSERT INTO connect_box (nombre, celular, email, mensaje, fecha_envio) VALUES (%s, %s, %s, %s, %s)"
        fecha_envio = datetime.now()
        valores = (nombre, celular, email, mensaje, fecha_envio)

        try:
            self.cursor.execute(sql, valores)
            self.conn.commit()
            messagebox.showinfo("Éxito", "Mensaje enviado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al enviar mensaje: {err}")

        self.cursor.close()
        self.conn.close()

    def mostrar_todos(self):
        self.conectar_base_datos()
        self.cursor.execute("SELECT * FROM connect_box")
        mensajes = self.cursor.fetchall()
        self.mostrar_resultado(mensajes)
        self.cursor.close()
        self.conn.close()

    def mostrar_por_id(self):
        self.conectar_base_datos()
        id_mensaje = self.id_var.get()

        try:
            id_mensaje = int(id_mensaje)
            self.cursor.execute(f"SELECT * FROM connect_box WHERE id = {id_mensaje}")
            mensaje = self.cursor.fetchone()

            if mensaje:
                self.mostrar_resultado([mensaje])
            else:
                messagebox.showinfo("Resultado", "No se encontró ningún mensaje con el ID proporcionado.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID válido.")

        self.cursor.close()
        self.conn.close()

    def eliminar_mensaje(self):
        self.conectar_base_datos()
        id_mensaje = self.id_var.get()

        try:
            id_mensaje = int(id_mensaje)
            self.cursor.execute(f"DELETE FROM connect_box WHERE id = {id_mensaje}")
            self.conn.commit()
            messagebox.showinfo("Éxito", "Mensaje eliminado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar mensaje: {err}")

        self.cursor.close()
        self.conn.close()

    def responder_mensaje(self):
        id_mensaje = self.id_var.get()

        try:
            id_mensaje = int(id_mensaje)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID válido.")
            return

        self.conectar_base_datos()

        # Obtener el mensaje por ID
        self.cursor.execute(f"SELECT * FROM connect_box WHERE id = {id_mensaje}")
        mensaje = self.cursor.fetchone()

        if mensaje:
            # Actualizar la interfaz con la información del mensaje
            self.nombre_var.set(mensaje['nombre'])
            self.celular_var.set(mensaje['celular'])
            self.email_var.set(mensaje['email'])
            self.mensaje_var.set(f"Re: {mensaje['mensaje']}")

            # Marcar el mensaje como leído
            self.cursor.execute(f"UPDATE connect_box SET leido = 1 WHERE id = {id_mensaje}")

            # Mostrar información de respuesta
            messagebox.showinfo("Responder Mensaje", f"Respondiendo al mensaje ID: {id_mensaje}")

            # Realizar la actualización en la base de datos
            gestion = f"Respuesta al mensaje ID {id_mensaje}"
            fecha_gestion = datetime.now()
            update_query = "UPDATE connect_box SET leido = 1, gestion = %s, fecha_gestion = %s WHERE id = %s"
            update_values = (gestion, fecha_gestion, id_mensaje)
            self.cursor.execute(update_query, update_values)
            self.conn.commit()

        else:
         
            messagebox.showinfo("Resultado", "No se encontró ningún mensaje con el ID proporcionado.")

        self.cursor.close()
        self.conn.close()

    def mostrar_resultado(self, mensajes):
        resultado = tk.Toplevel(self.master)
        resultado.title("Resultados")
        
        tk.Label(resultado, text="ID").grid(row=0, column=0)
        tk.Label(resultado, text="Nombre").grid(row=0, column=1)
        tk.Label(resultado, text="Celular").grid(row=0, column=2)
        tk.Label(resultado, text="Email").grid(row=0, column=3)
        tk.Label(resultado, text="Mensaje").grid(row=0, column=4)

        for i, mensaje in enumerate(mensajes, start=1):
            tk.Label(resultado, text=mensaje['id']).grid(row=i, column=0)
            tk.Label(resultado, text=mensaje['nombre']).grid(row=i, column=1)
            tk.Label(resultado, text=mensaje['celular']).grid(row=i, column=2)
            tk.Label(resultado, text=mensaje['email']).grid(row=i, column=3)
            tk.Label(resultado, text=mensaje['mensaje']).grid(row=i, column=4)

if __name__ == "__main__":
    # Crea una instancia de Tk y la aplicación MensajeApp
    root = tk.Tk()
    app = MensajeApp(root)
    root.mainloop()

