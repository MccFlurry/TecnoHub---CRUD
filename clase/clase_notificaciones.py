class Notificaciones:
    def __init__(self, id, usuario_id, mensaje, fecha_creacion, visto, usuario_nombre=None, usuario_foto=None):
        self.id = id
        self.usuario_id = usuario_id
        self.mensaje = mensaje
        self.fecha_creacion = fecha_creacion
        self.visto = visto
        self.usuario_nombre = usuario_nombre
        self.usuario_foto = usuario_foto

    def serialize(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'mensaje': self.mensaje,
            'fecha_creacion': self.fecha_creacion,
            'visto': self.visto,
            'usuario_nombre': self.usuario_nombre,
            'usuario_foto': self.usuario_foto
        }