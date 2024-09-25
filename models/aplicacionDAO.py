from models.conexion_db import ConexionDB
from models.usuario import usuario
from models.aplicacion import aplicacion
import cx_Oracle
import logging

class aplicacionDAO:
    @staticmethod
    def obtenerTodasApps():
        db = ConexionDB().get_connection()
        if db is None:
            logging.error("No se pudo obtener la conexión a la base de datos.")
            return None

        try:
            cursor = db.cursor()
            query = "SELECT IDAPP, NOMBRE FROM AUTOMATION.APLICACION ORDER BY NOMBRE ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            aplicaciones = [aplicacion(id=row[0], nombre=row[1]) for row in rows]
            return aplicaciones
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Error al obtener aplicaciones: {error.message}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def asignarAplicacion(usuario, id_app):
        try:
            
            db = ConexionDB().get_connection()
            if db is None:
                logging.error("No se pudo obtener la conexión a la base de datos.")
                return None
            
            query = """
            INSERT INTO AUTOMATION.USUARIO_APLICACION (IDUSERAPP, IDUSERFK, IDAPPFK, FECHA_ASIGNACION)
            VALUES (
                (SELECT NVL(MAX(IDUSERAPP), 0) + 1 FROM AUTOMATION.USUARIO_APLICACION),
                :iduser,
                :id_app,
                SYSDATE
            )

            """
            params = {
                'iduser': usuario['IDUSER'],
                'id_app': id_app
            }
            # Ejecutar la consulta
            with db.cursor() as cursor:
                cursor.execute(query, params)
                db.commit()
        except Exception as e:
            logging.error(f"Error al asignar aplicación: {str(e)}")
            raise

    @staticmethod
    def desvincularAplicacion(usuario, id_app):
        try:
            
            db = ConexionDB().get_connection()
            if db is None:
                logging.error("No se pudo obtener la conexión a la base de datos.")
                return None
            
            query = """
            UPDATE AUTOMATION.USUARIO_APLICACION UA
            SET FECHA_DESVINCULACION = SYSDATE
            WHERE UA.IDUSERFK = :iduser AND
                UA.IDAPPFK  = :idapp AND
                UA.FECHA_DESVINCULACION IS NULL
            """
            params = {
                'iduser': usuario,
                'idapp': id_app
            }
            # Ejecutar la consulta
            with db.cursor() as cursor:
                cursor.execute(query, params)
                db.commit()
        except Exception as e:
            logging.error(f"Error al asignar aplicación: {str(e)}")
            raise