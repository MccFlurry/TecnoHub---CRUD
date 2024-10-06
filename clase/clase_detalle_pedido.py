class DetallePedido:
    def __init__(self, id, pedido_id, producto_id, cantidad, precio_unitario):
        self.id = id
        self.pedido_id = pedido_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario