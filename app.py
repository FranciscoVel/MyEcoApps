from flask import Flask, render_template, send_file, after_this_request, redirect, request, session, url_for, jsonify
import subprocess
import os
import identity.web
import requests
import cx_Oracle
import logging
from models.usuarioDAO import usuarioDAO
from models.aplicacionDAO import aplicacionDAO
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
app.secret_key = 'MyEcoApps2024*'

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
@app.route('/asignacionApps1')
def asignacionApps1():
    return render_template('asignacionApps.html')

# Ruta para que el admin desvincule las aplicaciones al usuario
@app.route('/desvinculacionApps')
def desvinculacionApps():
    return render_template('desvinculacionApps.html')

# Ruta que busca el archivo a descargar
@app.route('/download')
def download_file():
    file_path = os.path.join(os.getcwd(),"instaladores", "main.exe")
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
    
#Ruta para buscar usuario en la BD o en el directorio activo y mostrar la informacion
@app.route('/buscarUsuario', methods=['POST'])
def buscarUsuario():
    data = request.get_json()
    registro = data.get('registro')
    verif = data.get('usuario')
    if registro:
        usuario = usuarioDAO.obtenerPorRegistro(registro)
        if isinstance(usuario, str) and verif == False:  # Si es una cadena, es el mensaje "buscar en el directorio activo" ACA SE DEBE BUSCAR EN EL DIRECTORIO ACTIVO Y DAR RESOUESTA
            #ACA DEBERA DAR UNA ALERTA DE QUE SE REGISTRO UN USUARIO NUEVO
            session['usuario'] = ''
            return jsonify({'mensaje': usuario})  
        
        # Si el usuario no esta en la BD pero se esta buscando desde la vista de usuario
        elif isinstance(usuario, str) and verif == True:
            return jsonify({'mensaje' : 'Usuario no encontrado, comuníquese con soporte'})
        
        else:
            usuarioDAO.cargarAplicaciones(usuario)

            session['usuario'] = usuario.to_dict()
            return jsonify(usuario.to_dict())
    

# Ruta para obtener todas las apps que un usuario en especifico se le pueden asignar
@app.route('/getAplicaciones', methods=['GET'])
def get_aplicaciones():
    try:
        # Obtener todas las aplicaciones de la base de datos
        aplicaciones = aplicacionDAO.obtenerTodasApps()
        aplicaciones_list = [app.to_dict() for app in aplicaciones] 
        
        # Obtener el usuario de la sesión
        usuario = session.get('usuario')
        
        # Obtener las aplicaciones asignadas al usuario
        aplicaciones_asignadas = usuario.get('APLICACIONES', []) if usuario else []
        
        # Extraer los IDs de las aplicaciones asignadas
        asignadas_ids = {app['IDAPP'] for app in aplicaciones_asignadas}
        
        # Filtrar la lista de aplicaciones para eliminar las asignadas
        aplicaciones_disponibles = [app for app in aplicaciones_list if app['IDAPP'] not in asignadas_ids]
                
        # Devolver la lista de aplicaciones disponibles
        return jsonify({'aplicaciones': aplicaciones_disponibles})
    
    except Exception as e:
        logging.error(f"Error al obtener aplicaciones: {str(e)}")
        return jsonify({'error': 'Error al obtener las aplicaciones'}), 500


#Ruta para cargar vista para que el admin asigne las apps correspondientes al usuario solicitante y enviar el usuario de registroUsuario a asignacionApps
@app.route('/asignacionApps')
def asignacionApps():
    usuario = session.get('usuario')  # Recuperar el usuario de la sesión
    if not usuario:
        return redirect(url_for('buscarUsuario'))  # Redirigir si no hay usuario en la sesión

    # Enviar el nombre y registro al HTML
    return render_template(
        'asignacionApps.html',
        nombre_usuario=usuario['NOMBRE'],
        registro_usuario=usuario['REGISTRO']
    )

# Ruta para hacer el insert en la BD de las aplicaciones que se le asiganaron a un usuario
@app.route('/asignarAplicaciones', methods=['POST'])
def asignarAplicaciones():
    data = request.get_json()
    usuario = session.get('usuario')
    aplicaciones = data.get('aplicaciones', [])

    if not usuario or not aplicaciones:
        return jsonify({'success': False, 'mensaje': 'Datos insuficientes'}), 400

    try:
        
        # Asignar aplicaciones al usuario
        for app in aplicaciones:
            app_id = app['IDAPP']
            aplicacionDAO.asignarAplicacion(usuario, app_id)

        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error al asignar aplicaciones: {str(e)}")
        return jsonify({'success': False, 'mensaje': 'Error al asignar aplicaciones'}), 500


@app.route('/desvincularApp', methods=['POST'])
def desvincularAplicaciones():
    data = request.get_json()
    usuario = session.get('usuario')
    aplicacion = data.get('aplicacion')

    try:
        logging.debug(usuario)
        aplicacionDAO.desvincularAplicacion(usuario['IDUSER'], aplicacion)

        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error al asignar aplicaciones: {str(e)}")
        return jsonify({'success': False, 'mensaje': 'Error al asignar aplicaciones'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
