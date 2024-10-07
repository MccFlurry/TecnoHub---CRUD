from bd import obtener_conexion
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor

# Inserta un nuevo producto en la base de datos
def insertar_producto(nombre, descripcion, categorias_id, precio, stock, destacado, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO productos (nombre, descripcion, categorias_id, precio, stock, destacado, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, categorias_id, precio, stock, destacado, imagen))
    conexion.commit()
    conexion.close()

# Obtiene un producto por su ID
def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, p.categorias_id, c.nombre as categorias
        FROM productos p
        JOIN categorias c ON p.categorias_id = c.id
        WHERE p.id = %s
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            producto = Producto(
                id=row['id'],
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                precio=row['precio'],
                stock=row['stock'],
                imagen=row['imagen'],
                categorias_id=row['categorias_id'],
                categorias=row['categorias']  # Nombre de la categoría
            )
    conexion.close()
    return producto

# Obtiene los productos que pertenecen a una categoría específica
def obtener_productos_por_categorias(categorias_id):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categorias_id, imagen FROM productos WHERE categorias_id = %s"
        cursor.execute(sql, (categorias_id,))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))  # Cada fila es un diccionario
    conexion.close()
    return productos

# Actualiza los detalles de un producto en la base de datos
def actualizar_producto(id, nombre, descripcion, precio, stock, categorias_id, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        UPDATE productos 
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categorias_id = %s, imagen = %s 
        WHERE id = %s
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, categorias_id, imagen, id))
    conexion.commit()
    conexion.close()

# Elimina un producto de la base de datos
def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

# Busca productos que coincidan con una consulta en nombre o descripción
def buscar_productos(query):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT id, nombre, descripcion, precio, stock, categorias_id, imagen 
        FROM productos 
        WHERE nombre LIKE %s OR descripcion LIKE %s
        """
        cursor.execute(sql, (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))  # Cada fila es un diccionario
    conexion.close()
    return productos

# Obtiene productos relacionados de la misma categoría
def obtener_productos_relacionados(producto_id, limite=4):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categorias_id, p.imagen 
        FROM productos p
        JOIN productos original ON p.categorias_id = original.categorias_id
        WHERE original.id = %s AND p.id != %s
        ORDER BY RAND()
        LIMIT %s
        """
        cursor.execute(sql, (producto_id, producto_id, limite))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))  # Cada fila es un diccionario
    conexion.close()
    return productos

# Obtiene todos los productos
def obtener_todos_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, p.categorias_id, c.nombre AS categorias_nombre
        FROM productos p
        JOIN categorias c ON p.categorias_id = c.id
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            producto = Producto(
                id=row['id'],
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                precio=row['precio'],
                stock=row['stock'],
                imagen=row['imagen'],
                categorias_id=row['categorias_id'],
                categorias=row['categorias_nombre']  # Aquí estás asignando el nombre de la categoría
            )
            productos.append(producto)
    conexion.close()
    return productos

# Realiza una búsqueda avanzada con múltiples filtros
def busqueda_avanzada(query=None, categorias_id=None, precio_min=None, precio_max=None):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categorias_id, p.imagen
        FROM productos p
        WHERE 1=1
        """
        params = []
        
        if query:
            sql += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
            params.extend(['%' + query + '%', '%' + query + '%'])
        
        if categorias_id:
            sql += " AND p.categorias_id = %s"
            params.append(categorias_id)
        
        if precio_min:
            sql += " AND p.precio >= %s"
            params.append(float(precio_min))
        
        if precio_max:
            sql += " AND p.precio <= %s"
            params.append(float(precio_max))
        
        cursor.execute(sql, params)
        productos = cursor.fetchall()
    
    conexion.close()
    return productos

# Obtiene productos recomendados
def obtener_productos_recomendados(producto_id, limite=4):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categorias_id, p.imagen
        FROM productos p
        JOIN productos original ON p.categorias_id = original.categorias_id
        WHERE original.id = %s AND p.id != %s
        ORDER BY RAND()
        LIMIT %s
        """, (producto_id, producto_id, limite))
        productos = cursor.fetchall()
    conexion.close()
    return productos

# Agrega una reseña a un producto
def agregar_opiniones(producto_id, usuario_id, calificacion, comentario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
        INSERT INTO opiniones (producto_id, usuario_id, calificacion, comentario)
        VALUES (%s, %s, %s, %s)
        """, (producto_id, usuario_id, calificacion, comentario))
    conexion.commit()
    conexion.close()

# Obtiene reseñas de un producto
def obtener_opinioness(producto_id):
    conexion = obtener_conexion()
    opinioness = []
    with conexion.cursor(DictCursor) as cursor:
        cursor.execute("""
        SELECT o.id, o.calificacion, o.comentario, o.fecha, u.nombre, u.apellido
        FROM opiniones o
        JOIN usuarios u ON o.usuario_id = u.id
        WHERE o.producto_id = %s
        ORDER BY o.fecha DESC
        """, (producto_id,))
        opinioness = cursor.fetchall()
    conexion.close()
    return opinioness

# Cuenta el total de productos en la base de datos
def contar_productos():
    conexion = obtener_conexion()
    total_productos = 0
    with conexion.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM productos"
        cursor.execute(sql)
        total_productos = cursor.fetchone()[0]  # Obtiene el total de productos
    conexion.close()
    return total_productos

# Obtiene productos destacados
def obtener_productos_destacados():
    conexion = obtener_conexion()
    productos_destacados = []
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, precio FROM productos WHERE destacado = 1"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            producto = {
                "id": row['id'],
                "nombre": row['nombre'],
                "precio": row['precio']
            }
            productos_destacados.append(producto)
    conexion.close()
    return productos_destacados
