class aplicacion:
    def __init__(self, id, nombre, ruta = None, imagen = None):
        self.id = id
        self.nombre = nombre
        self.ruta = ruta
        self.imagen = imagen

    def to_dict(self):
        return {
            'IDAPP': self.id,
            'NOMBRE': self.nombre,
            'RUTA': self.ruta,
            'IMAGEN': self.imagen
        }
