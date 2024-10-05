from bd import obtener_conexion

def insertar_producto(nombre, stock, precio, color, idMarca, idModelo, idCategoria):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO Producto(nombre, stock, precio, color, idMarca, idModelo, idCategoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, stock, precio, color, idMarca, idModelo, idCategoria))
    conexion.commit()
    conexion.close()

def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT idProducto, nombre, stock, precio, color, idMarca, idModelo, idCategoria 
        FROM Producto
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
    conexion.close()
    return productos

def eliminar_producto(idProducto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Producto WHERE idProducto = %s", (idProducto,))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(idProducto):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        sql = """
        SELECT idProducto, nombre, stock, precio, color, idMarca, idModelo, idCategoria 
        FROM Producto WHERE idProducto = %s
        """
        cursor.execute(sql, (idProducto,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def actualizar_producto(nombre, stock, precio, color, idMarca, idModelo, idCategoria, idProducto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        UPDATE Producto 
        SET nombre = %s, stock = %s, precio = %s, color = %s, idMarca = %s, idModelo = %s, idCategoria = %s 
        WHERE idProducto = %s
        """
        cursor.execute(sql, (nombre, stock, precio, color, idMarca, idModelo, idCategoria, idProducto))
    conexion.commit()
    conexion.close()