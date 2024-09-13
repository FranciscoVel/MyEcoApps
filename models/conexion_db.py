import cx_Oracle
import logging

class ConexionDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConexionDB, cls).__new__(cls)
            try:
                cls._instance.connection = cx_Oracle.connect(
                    user='AUTOMATION',
                    password='ECpetr02_#2024',
                    dsn='10.232.88.28/geoxdb'
                )
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                logging.error(f"Error al conectarse a la base de datos: {error.message}")
                cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        if self.connection:
            return self.connection
        else:
            logging.error("No se pudo establecer una conexión a la base de datos.")
            return None

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                logging.error(f"Error al cerrar la conexión a la base de datos: {error.message}")
