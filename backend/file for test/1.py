import mysql.connector
import datetime

class Mensaje:

    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database  # Se agregó el parámetro 'database'
        )
        self.cursor = self.conn.cursor(dictionary=True)

        # Se utiliza un bloque try-except para manejar errores al seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Se corrigió el nombre de la tabla a 'connect_box' en lugar de 'connect_box1'
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS connect_box (
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

    def enviar_mensaje(self, nombre, celular, email, mensaje):
        sql = "INSERT INTO connect_box (nombre, celular, email, mensaje, fecha_envio) VALUES (%s, %s, %s, %s, %s)"
        fecha_envio = datetime.datetime.now()
        valores = (nombre, celular, email, mensaje, fecha_envio)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def listar_mensajes(self):
        self.cursor.execute("SELECT * FROM connect_box")
        mensajes = self.cursor.fetchall()
        return mensajes

    def responder_mensaje(self, id, gestion):
        fecha_gestion = datetime.datetime.now()
        sql = "UPDATE connect_box SET leido = 1, gestion = %s, fecha_gestion = %s WHERE id = %s"
        valores = (gestion, fecha_gestion, id)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_mensaje(self, id):
        self.cursor.execute(f"DELETE FROM connect_box WHERE id = {id}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def mostrar_mensaje(self, id):
         sql = f"SELECT id, nombre, celular, email, mensaje, fecha_envio, leido, gestion, fecha_gestion FROM connect_box WHERE id = {id}"
         self.cursor.execute(sql)
         return self.cursor.fetchone()

mensaje = Mensaje("localhost", "root", "", "bakers_box")
id = int(input("Ingrese id del mensaje que quiere ver: "))
respuesta = mensaje.mostrar_mensaje(id)

print(respuesta)