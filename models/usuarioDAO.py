from models.conexion_db import ConexionDB
from models.usuario import usuario
import cx_Oracle
import logging


logging.basicConfig(filename='usuarioDAO.log', level=logging.DEBUG)

class usuarioDAO:
    @staticmethod
    def obtener_por_registro(registro):
        db = ConexionDB().get_connection()
        if db is None:
            logging.error("No se pudo obtener la conexión a la base de datos.")
            return None
        try:
            cursor = db.cursor()
            query = "SELECT IDUSER, NOMBRE, CORREO, ROL, REGISTRO FROM USUARIO WHERE REGISTRO = :registro"
            cursor.execute(query, registro=registro)
            row = cursor.fetchone()
            if row:
                return usuario(
                    id=row[0],
                    nombre=row[1],
                    correo=row[2],
                    rol=row[3],
                    registro=row[4]
                )
            else:
                return None
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Error al realizar la consulta: {error.message}")
            return None
        finally:
            cursor.close()
