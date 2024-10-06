class Opinion:
    def __init__(self, id, producto_id, usuario_id, comentario, calificacion, fecha):
        self.id = id
        self.producto_id = producto_id
        self.usuario_id = usuario_id
        self.comentario = comentario
        self.calificacion = calificacion
        self.fecha = fecha