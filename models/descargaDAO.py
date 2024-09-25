from models.conexion_db import ConexionDB
import logging
class descargaDAO:
    @staticmethod
    def registrarFechaDescarga(usuario, id_app):
        try:
            
            db = ConexionDB().get_connection()
            if db is None:
                logging.error("No se pudo obtener la conexión a la base de datos.")
                return None
            logging.debug(id_app)
            
            query = """
            INSERT INTO AUTOMATION.DESCARGAS_APLICACION (IDDESCARGA, IDUSERAPPFK, FECHA_DESCARGA)
            VALUES ((SELECT NVL(MAX(IDDESCARGA), -1) + 1 FROM AUTOMATION.DESCARGAS_APLICACION),
            (SELECT IDUSERAPP FROM AUTOMATION.USUARIO_APLICACION
                WHERE IDUSERFK = :iduser AND
                IDAPPFK = :idapp AND
                fecha_desvinculacion IS NULL),
                SYSDATE
            )
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
            logging.error(f"Error al registrar fecha de descarga aplicación: {str(e)}")
            raise