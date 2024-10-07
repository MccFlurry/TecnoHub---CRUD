class Producto:
    def __init__(self, id, nombre, descripcion, precio, stock, imagen, categorias_id=None, categorias=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
        self.categorias_id = categorias_id
        self.categorias = categorias  #Nombre de la categoría
