class Opinion:
    def __init__(self, id, producto_id, usuario_id, comentario, calificacion, fecha):
        self.id = id
        self.producto_id = producto_id
        self.usuario_id = usuario_id
        self.comentario = comentario
        self.calificacion = calificacion
        self.fecha = fecha
        self.nombre_usuario = None

    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'usuario_id': self.usuario_id,
            'comentario': self.comentario,
            'calificacion': self.calificacion,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S') if self.fecha else None,
            'nombre_usuario': self.nombre_usuario
        }