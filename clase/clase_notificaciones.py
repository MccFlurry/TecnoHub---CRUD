class Notificaciones:
    def __init__(self, id, usuario_id, mensaje, fecha_creacion, visto, usuario_nombre=None):
        self.id = id
        self.usuario_id = usuario_id
        self.mensaje = mensaje
        self.fecha_creacion = fecha_creacion
        self.visto = visto
        self.usuario_nombre = usuario_nombre
