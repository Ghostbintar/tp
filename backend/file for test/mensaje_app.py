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
        self.nombre_var = tk.StringVar()
        self.celular_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.mensaje_var = tk.StringVar()

        # Crear los elementos de la interfaz
        tk.Label(master, text="Nombre:").grid(row=0, column=0, sticky=tk.E)
        tk.Label(master, text="Celular:").grid(row=1, column=0, sticky=tk.E)
        tk.Label(master, text="Email:").grid(row=2, column=0, sticky=tk.E)
        tk.Label(master, text="Mensaje:").grid(row=3, column=0, sticky=tk.E)

        tk.Entry(master, textvariable=self.nombre_var).grid(row=0, column=1)
        tk.Entry(master, textvariable=self.celular_var).grid(row=1, column=1)
        tk.Entry(master, textvariable=self.email_var).grid(row=2, column=1)
        tk.Entry(master, textvariable=self.mensaje_var).grid(row=3, column=1)

        tk.Button(master, text="Enviar Mensaje", command=self.enviar_mensaje).grid(row=4, column=0, columnspan=2, pady=10)

    def conectar_base_datos(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bakers_box"
            )
            self.cursor = self.conn.cursor()
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

if __name__ == "__main__":
    # Crea una instancia de Tk y la aplicación MensajeApp
    root = tk.Tk()
    app = MensajeApp(root)
    root.mainloop()
