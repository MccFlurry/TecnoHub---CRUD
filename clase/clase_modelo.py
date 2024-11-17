class Modelo:
    def __init__(self, nombre="", id=None):
        self.id = id
        self.nombre = nombre

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }
