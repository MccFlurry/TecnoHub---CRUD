class Pais:
    def __init__(self, id=None, nombre=None, codigo_iso=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.codigo_iso = codigo_iso
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo_iso': self.codigo_iso,
            'activo': self.activo
        }
