class Producto:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, stock=0, categoria_id=None, id_marca=None, id_modelo=None, destacado=None, imagen=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = 0 if stock is None else int(stock)  # Asegurar que stock sea siempre un entero
        self.categoria_id = categoria_id
        self.id_marca = id_marca
        self.id_modelo = id_modelo
        self.destacado = destacado
        self.imagen = imagen

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'categoria_id': self.categoria_id,
            'id_marca': self.id_marca,
            'id_modelo': self.id_modelo,
            'destacado': self.destacado,
            'imagen': self.imagen
        }
