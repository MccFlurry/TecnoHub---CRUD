class Distrito:
    def __init__(self, id=None, ciudad_id=None, nombre=None, activo=True):
        self.id = id
        self.ciudad_id = ciudad_id
        self.nombre = nombre
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'ciudad_id': self.ciudad_id,
            'nombre': self.nombre,
            'activo': self.activo
        }