class Kit:
    def __init__(self, id, usuario_id, celular_id, smartwatch_id, accesorios_id, fecha_creacion):
        self.id = id
        self.usuario_id = usuario_id
        self.celular_id = celular_id
        self.smartwatch_id = smartwatch_id
        self.accesorios_id = accesorios_id
        self.fecha_creacion = fecha_creacion

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'celular_id': self.celular_id,
            'smartwatch_id': self.smartwatch_id,
            'accesorios_id': self.accesorios_id,
            'fecha_creacion': str(self.fecha_creacion),
            'celular': self.celular.to_dict() if hasattr(self, 'celular') else None,
            'smartwatch': self.smartwatch.to_dict() if hasattr(self, 'smartwatch') else None,
            'accesorios': self.accesorios.to_dict() if hasattr(self, 'accesorios') else None
        }