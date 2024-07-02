#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

#Creo instancia de la Clase Flask
app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

class Cliente:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            correo VARCHAR(255) NOT NULL,
            telefono INT NOT NULL,
            mensaje VARCHAR(255),
            imagen_url VARCHAR(255),
            contacto VARCHAR(255) NOT NULL,
            turno_dia VARCHAR(255) NOT NULL,
            turno_hora TIME NOT NULL,
            novedad VARCHAR(255)''')
        self.conn.commit()
        
        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def listar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        return clientes
    
    def consultar_cliente(self, codigo):
        # Consultamos un cliente a partir de su código
        self.cursor.execute(f"SELECT * FROM clientes WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    def mostrar_cliente(self, codigo):
        # Mostramos los datos de un cliente a partir de su código
        cliente = self.consultar_cliente(codigo)
        if cliente:
            print("-" * 40)
            print(f"Código............: {cliente['codigo']}")
            print(f"Nombre y Apellido.: {cliente['nombre']}")
            print(f"Correo electrónico: {cliente['correo']}")
            print(f"Teléfono..........: {cliente['telefono']}")
            print(f"Mensaje...........: {cliente['mensaje']}")
            print(f"Imagen............: {cliente['imagen_url']}")
            print(f"Contacto..........: {cliente['contacto']}")
            print(f"Turno día.........: {cliente['turno_dia']}")
            print(f"Turno hora........: {cliente['turno_hora']}")
            print("-" * 40)
        else:
            print("Cliente no encontrado.")

    def agregar_cliente(self, nombre, correo, telefono, mensaje, imagen_url, contacto, turno_dia, turno_hora, novedad):
        sql = "INSERT INTO clientes (nombre, correo, telefono, mensaje, imagen_url, contacto, turno_dia, turno_hora, novedad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, correo, telefono, mensaje, imagen_url, contacto, turno_dia, turno_hora, novedad)

        self.cursor.execute(sql,valores)
        self.conn.commit()
        return self.cursor.lastrowid

    def modificar_cliente(self, codigo, nuevo_correo, nuevo_telefono, nuevo_mensaje, nueva_imagen, nuevo_turno_dia, nuevo_turno_hora):
        sql = "UPDATE clientes SET correo = %s, telefono = %s, mensaje = %s, imagen_url = %s, turno_dia = %s, turno_hora = %s WHERE codigo = %s"
        valores = (nuevo_correo, nuevo_telefono, nuevo_mensaje, nueva_imagen, nuevo_turno_dia, nuevo_turno_hora, codigo)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar_cliente(self, codigo):
        # Eliminamos un cliente de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM clientes WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Cliente
cliente = Cliente(host='localhost', user='root', password='sergiusdba', database='miapp')
#catalogo = Catalogo(host='juanpablocodo.mysql.pythonanywhere-services.com', user='juanpablocodo', password='root-123456', database='juanpablocodo$miapp')

# Carpeta para guardar las imagenes
ruta_destino = './static/imagenes/'
#ruta_destino = '/home/juanpablocodo/mysite/static/imagenes/'

# Lista completa de clientes
@app.route("/clientes", methods=["GET"])  #GET nos trae los clientes
def listar_clientes():
    clientes = cliente.listar_clientes()  #lista de diccionarios con los clientes
    return jsonify(clientes)  #convierto a json el diccionario

# Muestra un cliente
@app.route("/clientes/<int:codigo>", methods=["GET"])  #traigo solo un código de cliente
def mostrar_cliente(codigo):
    cliente = cliente.consultar_cliente(codigo)
    if cliente:
        return jsonify(cliente)  #lista de diccionario de clientes
    else:
        return "Cliente no encontrado", 404

# Agrega nuevo cliente
@app.route("/clientes", methods=["POST"])
def agregar_cliente():
    #Recojo los datos del form
    nombre = request.form['nombreApellido']
    correo = request.form['correoElectronico']
    telefono = request.form['telefono']
    mensaje = request.form['mensaje']
    imagen = request.files['formFile']
    contacto = request.form[input[5].get('value')]
    turno_dia = request.form['dia']
    turno_hora = request.form['hora']
    novedad = request.form['info'].value
    nombre_imagen = ""

    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename)
    nombre_base, extension = os.path.splitext(nombre_imagen)
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    nuevo_codigo = cliente.agregar_cliente(nombre, correo, telefono, mensaje, nombre_imagen, contacto, turno_dia, turno_hora, novedad)
    if nuevo_codigo:
        imagen.save(os.path.join(ruta_destino, nombre_imagen))
        return jsonify({"mensaje": "Cliente agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        return jsonify({"mensaje": "Error al agregar el cliente."}), 500

# Modificar datos del cliente
@app.route("/clientes/<int:codigo>", methods=["PUT"])
def modificar_cliente(codigo):
    #Se recuperan los nuevos datos del formulario
    nuevo_correo = request.form.get("correoElectronico")
    nuevo_telefono = request.form.get("telefono")
    nuevo_mensaje = request.form.get("mensaje")
    nuevo_turno_dia = request.form.get("dia")
    nuevo_turno_hora = request.form.get("hora")

    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) 
        nombre_base, extension = os.path.splitext(nombre_imagen) 
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" 

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(ruta_destino, nombre_imagen))

        # Busco el cliente guardado
        cliente = cliente.consultar_cliente(codigo)
        if cliente: # Si existe el cliente...
            imagen_vieja = cliente["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(ruta_destino, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    else:
        cliente = cliente.consultar_cliente(codigo)
        if cliente:
            nombre_imagen = cliente["imagen_url"]

   # Se llama al método modificar_cliente pasando el codigo del cliente y los nuevos datos.
    if cliente.modificar_cliente(codigo, nuevo_correo, nuevo_telefono, nuevo_mensaje, nombre_imagen, nuevo_turno_dia, nuevo_turno_hora):
        return jsonify({"mensaje": "Cliente modificado"}), 200
    else:
        return jsonify({"mensaje": "Cliente no encontrado"}), 403

# Borrar un cliente
@app.route("/clientes/<int:codigo>", methods=["DELETE"])
def eliminar_cliente(codigo):
    # Primero, obtiene la información del cliente para encontrar la imagen
    cliente = cliente.consultar_cliente(codigo)
    if cliente:
        # Eliminar la imagen asociada si existe
        ruta_imagen = os.path.join(ruta_destino, cliente['imagen_url'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el cliente
        if cliente.eliminar_cliente(codigo):
            return jsonify({"mensaje": "Cliente eliminado"}), 200
        else:
            return jsonify({"mensaje": "Error al eliminar el cliente"}), 500
    else:
        return jsonify({"mensaje": "Cliente no encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True)