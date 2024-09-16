from models.aplicacion import aplicacion
class usuario:
    def __init__(self, registro, id=None, nombre=None, correo=None, rol=None):
        self.id = id
        self.nombre = nombre
        self.registro = registro
        self.correo = correo
        self.rol = rol
        self.aplicaciones = []  # Lista para almacenar aplicaciones

    def agregar_aplicacion(self, aplicacion1):
        """Agrega una aplicación a la lista de aplicaciones del usuario."""
        if isinstance(aplicacion1, aplicacion):
            self.aplicaciones.append(aplicacion1)

    def eliminar_aplicacion(self, aplicacion_id):
        """Elimina una aplicación de la lista por su ID."""
        self.aplicaciones = [app for app in self.aplicaciones if app.id != aplicacion_id]

    def obtener_aplicaciones(self):
        """Retorna la lista de aplicaciones del usuario."""
        return self.aplicaciones

    def to_dict(self):
        return {
            'IDUSER': self.id,
            'NOMBRE': self.nombre,
            'CORREO': self.correo,
            'ROL': self.rol,
            'REGISTRO': self.registro,
            'APLICACIONES': [app.to_dict() for app in self.aplicaciones]
        }

