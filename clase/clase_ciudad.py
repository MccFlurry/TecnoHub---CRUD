class Ciudad:
    def __init__(self, id=None, estado_id=None, nombre=None, codigo_postal_patron=None, activo=True):
        self.id = id
        self.estado_id = estado_id
        self.nombre = nombre
        self.codigo_postal_patron = codigo_postal_patron
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'estado_id': self.estado_id,
            'nombre': self.nombre,
            'codigo_postal_patron': self.codigo_postal_patron,
            'activo': self.activo
        }