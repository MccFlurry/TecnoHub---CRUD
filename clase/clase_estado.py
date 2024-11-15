class Estado:
    def __init__(self, id=None, pais_id=None, nombre=None, codigo=None, activo=True):
        self.id = id
        self.pais_id = pais_id
        self.nombre = nombre
        self.codigo = codigo
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'pais_id': self.pais_id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'activo': self.activo
        }