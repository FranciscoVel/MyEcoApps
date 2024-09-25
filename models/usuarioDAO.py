from models.conexion_db import ConexionDB
from models.usuario import usuario
from models.aplicacion import aplicacion
import cx_Oracle
import logging


logging.basicConfig(filename='usuarioDAO.log', level=logging.DEBUG)

class usuarioDAO:
    @staticmethod
    def obtenerPorRegistro(registro):
        db = ConexionDB().get_connection()
        if db is None:
            logging.error("No se pudo obtener la conexión a la base de datos.")
            return None  # Aquí mantenemos el retorno como None si no hay conexión
        
        try:
            cursor = db.cursor()
            query = "SELECT IDUSER, NOMBRE, CORREO, ROL, REGISTRO FROM AUTOMATION.USUARIO WHERE REGISTRO = :registro"
            cursor.execute(query, registro=registro)
            row = cursor.fetchone()
            if row:  # Si hay resultados, creamos el objeto usuario

                user = usuario(
                    id=row[0],
                    nombre=row[1],
                    correo=row[2],
                    rol=row[3],
                    registro=row[4])
                logging.debug('hola')
                logging.debug(user)
                return user
            else:
                
                return "Usuario no encontrado. Buscando en el directorio activo."  # Devolver el mensaje como string

        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Error al realizar la consulta: {error.message}")
            return None  # En caso de error, devolver None
        
        finally:
            cursor.close()

    @staticmethod
    def obtenerPorMail(mail):
        db = ConexionDB().get_connection()
        if db is None:
            logging.error("No se pudo obtener la conexión a la base de datos.")
            return None  # Aquí mantenemos el retorno como None si no hay conexión
        
        try:
            cursor = db.cursor()
            query = "SELECT IDUSER, NOMBRE, CORREO, ROL, REGISTRO FROM AUTOMATION.USUARIO WHERE CORREO = :mail"
            cursor.execute(query, mail=mail)
            row = cursor.fetchone()
            if row:  # Si hay resultados, creamos el objeto usuario
                return usuario(
                    id=row[0],
                    nombre=row[1],
                    correo=row[2],
                    rol=row[3],
                    registro=row[4]
                )
            else:
                
                return "Usuario no encontrado."  # Devolver el mensaje como string

        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Error al realizar la consulta: {error.message}")
            return None  # En caso de error, devolver None
        
        finally:
            cursor.close()


    @staticmethod
    def cargarAplicaciones(usuario):

        db = ConexionDB().get_connection()
        if db is None:
            logging.error("No se pudo obtener la conexión a la base de datos.")
            return None
        try:
            cursor = db.cursor()
            
            # Consulta para obtener las aplicaciones asociadas al usuario
            query_aplicaciones = """
                SELECT A.IDAPP, A.NOMBRE, A.RUTA, A.IMAGEN
                FROM AUTOMATION.APLICACION A
                INNER JOIN AUTOMATION.USUARIO_APLICACION UA ON UA.IDAPPFK = A.IDAPP
                INNER JOIN AUTOMATION.USUARIO U ON U.IDUSER = UA.IDUSERFK
                WHERE U.REGISTRO = :registro AND
                      UA.FECHA_DESVINCULACION IS NULL
                ORDER BY A.NOMBRE ASC
            """
            cursor.execute(query_aplicaciones, registro=usuario.registro)
            rows = cursor.fetchall()
            
            for row in rows:
                aplicacion_obj = aplicacion(
                    id=row[0],  
                    nombre=row[1],
                    ruta=row[2], 
                    imagen=row[3]
                )
                usuario.agregar_aplicacion(aplicacion_obj)
        
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Error al realizar la consulta de aplicaciones: {error.message}")
        
        finally:
            cursor.close()

    @staticmethod
    def registrarUsuario(usuario):
        try:
            
            db = ConexionDB().get_connection()
            if db is None:
                logging.error("No se pudo obtener la conexión a la base de datos.")
                return None
            
            query = """
            INSERT INTO AUTOMATION.USUARIO (IDUSER, NOMBRE, CORREO, ROL, REGISTRO)
            VALUES (
                (SELECT NVL(MAX(IDUSER), -1) + 1 FROM AUTOMATION.USUARIO),
                :nombre,
                :correo,
                'USER',
                :registro
            )

            """
            params = {
                'nombre': usuario['NOMBRE'],
                'correo': usuario['CORREO'],
                'registro': usuario['REGISTRO']
            }
            # Ejecutar la consulta
            with db.cursor() as cursor:
                cursor.execute(query, params)
                db.commit()
        except Exception as e:
            logging.error(f"Error al asignar aplicación: {str(e)}")
            raise

