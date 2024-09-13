from flask import Flask, render_template, send_file, after_this_request, redirect, request, session, url_for, jsonify
import subprocess
import os
import identity.web
import requests
import cx_Oracle
import logging
from models.usuarioDAO import usuarioDAO
from models.conexion_db import ConexionDB
from flask_session import Session
import app_config
from app_config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, SCOPE
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv


load_dotenv()  # Cargar las variables de entorno desde el archivo .env


__version__ = "1.0.0"  # constante para controlar versionamiento


# configuracion de carpeta Templates (html's)
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'Templates')

# Inicializacion de app flask
app = Flask(__name__, template_folder=template_dir)

# middleware para corregir el esquema de dirección URL y la información del host en los encabezados de solicitud.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config.from_object(app_config)
assert app.config["REDIRECT_PATH"] != "/", "REDIRECT_PATH must not be /"
Session(app)

# Inicialización de un objeto de autenticación con los datos del archivo app en azure, se toman directamente del archivo .env
app.jinja_env.globals.update(Auth=identity.web.Auth) 
auth = identity.web.Auth(
    session=session,
    authority=os.getenv("AUTHORITY"),
    client_id=os.getenv("CLIENT_ID"),
    client_credential=os.getenv("CLIENT_SECRET"),
)

logging.basicConfig(filename='mi_app.log', level=logging.DEBUG)

# Archivo raiz
@app.route('/')
def index():
    return render_template("inicioSesion.html", version=__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))   

# Ruta para como ususario ver las aplicaciones asignadas, agregar la parte del manual
@app.route('/aplicaciones')
def aplicaciones():
    return render_template('aplicaciones.html')

# Ruta para como admin registrar usuario solicitante
@app.route('/registroUsuario')
def registroUsuario():
    return render_template('registroUsuario.html')

# Ruta para que el admin asigne las apps correspondientes al usuario solicitante
@app.route('/asignacionApps')
def asignacionApps():
    return render_template('asignacionApps.html')

# Ruta para que el admin desvincule las aplicaciones al usuario
@app.route('/desvinculacionApps')
def desvinculacionApps():
    return render_template('desvinculacionApps.html')

# Ruta que busca el archivo a descargar
@app.route('/download')
def download_file():
    file_path = os.path.join(os.getcwd(), "main.exe")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Archivo no encontrado", 404

# Ruta para Iniciar sesion
@app.route('/login')
def login():
    return render_template("login.html", version=__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))


# Ruta que controla la respuesta del login y redirige a las aplicaciones (se debe redirigir segun sea su rol)
@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))

# Ruta para cerrar sesion
@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

# Ruta para obtener JSON de la API de microsoft
@app.route("/call_downstream_api")
def call_downstream_api():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    # Use access token to call downstream api
    api_result = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        timeout=30,
    ).json()
    return render_template('display.html', result=api_result)


@app.route('/conexion')
def conexion():
    db = ConexionDB().get_connection()
    if db is None:
        return "No se pudo obtener la conexión a la base de datos."
    try:
        cursor = db.cursor()
        query = "SELECT IDUSER, NOMBRE, CORREO, ROL, REGISTRO FROM USUARIO WHERE REGISTRO = :registro"
        cursor.execute(query, registro='C123456')
        return "conexion exitosa"
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return f"Error al realizar la consulta: {error.message}"
    finally:
        cursor.close()
    

@app.route('/buscarUsuario', methods=['POST'])
def buscarUsuario():
    logging.debug("Holaaaaaaa")

    data = request.get_json()
    registro = data.get('registro')
    if registro:
        usuario = usuarioDAO.obtener_por_registro(registro)
    # Retornando un JSON de prueba para verificar la funcionalidad
    return jsonify({
        'IDUSER': 123,
        'NOMBRE': 'Usuario Prueba',
        'CORREO': 'usuario@prueba.com',
        'ROL': usuario.id,
        'REGISTRO': registro
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
