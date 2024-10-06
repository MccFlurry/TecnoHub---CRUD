class Pedido:
    def __init__(self, id, usuario_id, fecha_pedido, estado):
        self.id = id
        self.usuario_id = usuario_id
        self.fecha_pedido = fecha_pedido
        self.estado = estado