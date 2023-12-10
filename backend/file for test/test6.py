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

        # Nueva variable de instancia para almacenar el número de mensajes
        self.numero_mensajes_anterior = 0

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

        tk.Button(master, text="Eliminar Mensaje", command=self.ventana_eliminar).grid(row=6, column=0, columnspan=2)
        tk.Button(master, text="Responder Mensaje", command=self.ventana_responder).grid(row=7, column=0, columnspan=2, pady=10)

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
            # Llama a la función para verificar nuevos mensajes
            self.verificar_nuevos_mensajes()
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

    def mostrar_resultado(self, mensajes):
        for mensaje in mensajes:
            print(mensaje)

    def ventana_eliminar(self):
        id_mensaje = self.id_var.get()
        if not id_mensaje:
            messagebox.showerror("Error", "Por favor, ingresa un ID de mensaje.")
            return

        respuesta = messagebox.askquestion("Eliminar Mensaje", f"¿Estás seguro de eliminar el mensaje con ID {id_mensaje}?")
        if respuesta == "yes":
            self.eliminar_mensaje(id_mensaje)

    def ventana_responder(self):
        id_mensaje = self.id_var.get()
        if not id_mensaje:
            messagebox.showerror("Error", "Por favor, ingresa un ID de mensaje para responder.")
            return

        # Puedes abrir una nueva ventana aquí para la respuesta

    def eliminar_mensaje(self, id_mensaje):
        self.conectar_base_datos()

        try:
            self.cursor.execute(f"DELETE FROM connect_box WHERE id = {id_mensaje}")
            self.conn.commit()
            messagebox.showinfo("Éxito", "Mensaje eliminado correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar mensaje: {err}")

        self.cursor.close()
        self.conn.close()

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

    def verificar_nuevos_mensajes(self):
        self.conectar_base_datos()
        self.cursor.execute("SELECT COUNT(*) FROM connect_box")
        numero_mensajes_actual = self.cursor.fetchone()[0]

        # Compara el número de mensajes antes y después
        if numero_mensajes_actual > self.numero_mensajes_anterior:
            # Hay nuevos mensajes, muestra una notificación
            messagebox.showinfo("Nuevos Mensajes", "¡Tienes nuevos mensajes!")

        # Actualiza el número anterior de mensajes
        self.numero_mensajes_anterior = numero_mensajes_actual

        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    # Crea una instancia de Tk y la aplicación MensajeApp
    root = tk.Tk()
    app = MensajeApp(root)
    root.mainloop()
