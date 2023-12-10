# Instalar con pip install Flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class Mensaje:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mi_tabla (
            id int(11) NOT NULL AUTO_INCREMENT,
            nombre varchar(30) NOT NULL,
            celular varchar(15) NOT NULL,
            email varchar(60) NOT NULL,
            mensaje varchar(500) NOT NULL,
            fecha_envio datetime NOT NULL,
            leido tinyint(1) NOT NULL,
            gestion varchar(500) DEFAULT NULL,
            fecha_gestion datetime DEFAULT NULL,
            PRIMARY KEY(`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
            ''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def enviar_mensaje(self, nombre, celular, email, consulta):
        sql = "INSERT INTO mi_tabla(nombre, celular, email, mensaje, fecha_envio) VALUES (%s, %s, %s, %s, %s)"
        fecha_envio = datetime.now()
        valores = (nombre, celular, email, consulta, fecha_envio)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def listar_mensajes(self):
        self.cursor.execute("SELECT * FROM mi_tabla")
        mensajes = self.cursor.fetchall()
        return mensajes

    def responder_mensaje(self, id, gestion):
        fecha_gestion = datetime.now()
        sql = "UPDATE mi_tabla SET leido = 1, gestion = %s, fecha_gestion = %s WHERE id = %s"
        valores = (gestion, fecha_gestion, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_mensaje(self, id):
        self.cursor.execute(f"DELETE FROM mi_tabla WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mostrar_mensaje(self, id):
         sql = f"SELECT id, nombre, celular, email, mensaje, fecha_envio, leido, gestion, fecha_gestion FROM mi_tabla WHERE id = {id}"
         self.cursor.execute(sql)
         return self.cursor.fetchone()

mensaje = Mensaje(host='localhost', user='root', password='', database='mi_database')

@app.route("/mensajes", methods=["GET"])
def listar_mensajes():
    respuesta = mensaje.listar_mensajes()
    return jsonify(respuesta)

@app.route("/mensajes", methods=["POST"])
def agregar_mensaje():
    nombre = request.form['nombre']
    celular = request.form['celular']
    email = request.form['email']
    consulta = request.form['mensaje']

    if mensaje.enviar_mensaje(nombre, celular, email, consulta):
        return jsonify({"mensaje": "Mensaje agregado"}), 201
    else:
        return jsonify({"mensaje": "No fue posible registrar el mensaje"}), 400

@app.route("/mensajes/<int:id>", methods=["PUT"])
def responder_mensaje(id):
    gestion = request.form.get("gestion")
    
    if mensaje.responder_mensaje(id, gestion):
        return jsonify({"mensaje": "Mensaje modificado"}), 200
    else:
        return jsonify({"mensaje": "Mensaje no encontrado"}), 403

if __name__ == "__main__":
    app.run(debug=True)
