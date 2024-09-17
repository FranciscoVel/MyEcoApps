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
            logging.debug(row)
            if row:  # Si hay resultados, creamos el objeto usuario
                return usuario(
                    id=row[0],
                    nombre=row[1],
                    correo=row[2],
                    rol=row[3],
                    registro=row[4]
                )
            else:
                
                return "Usuario no encontrado. Buscar en el directorio activo."  # Devolver el mensaje como string

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
                WHERE U.REGISTRO = :registro
            """
            cursor.execute(query_aplicaciones, registro=usuario.registro)
            rows = cursor.fetchall()
            
            for row in rows:
                logging.debug(row)
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

