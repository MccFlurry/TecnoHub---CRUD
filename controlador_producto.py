from bd import obtener_conexion
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor

# Inserta un nuevo producto en la base de datos
def insertar_producto(nombre, descripcion, categoria_id, precio, stock, destacado, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO productos (nombre, descripcion, categoria_id, precio, stock, destacado, imagen)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, categoria_id, precio, stock, destacado, imagen))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen, categoria_id FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()

    if producto:
        return Producto(
            id=producto[0],
            nombre=producto[1],
            descripcion=producto[2],
            precio=producto[3],
            stock=producto[4],
            imagen=producto[5],
            categoria_id=producto[6]
        )
    return None

def obtener_productos_por_categorias(categoria_id):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos WHERE categoria_id = %s"
        cursor.execute(sql, (categoria_id,))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))  # Cada fila es un diccionario
    conexion.close()
    return productos

#Función para obtener productos por categoría para el home
def obtener_productos_por_ids(ids):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        # Genera una consulta SQL para obtener múltiples productos
        sql = "SELECT id, nombre, descripcion, precio, stock, imagen, categoria_id FROM productos WHERE id IN ({})".format(
            ', '.join(['%s'] * len(ids))
        )
        cursor.execute(sql, ids)
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))
    conexion.close()
    return productos

# Actualiza los detalles de un producto en la base de datos
def actualizar_producto(id, nombre, descripcion, precio, stock, categoria_id, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        UPDATE productos 
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria_id = %s, imagen = %s 
        WHERE id = %s
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, categoria_id, imagen, id))
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
# Ejemplo de la función buscar_productos
def buscar_productos(query):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen 
        FROM productos 
        WHERE nombre LIKE %s OR descripcion LIKE %s
        """
        cursor.execute(sql, (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))
    conexion.close()
    return productos

# Obtiene productos relacionados de la misma categoría
def obtener_productos_relacionados(producto_id, limite=4):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categoria_id, p.imagen 
        FROM productos p
        JOIN productos original ON p.categoria_id = original.categoria_id
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
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, p.categoria_id, c.nombre AS categoria_nombre
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
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
                categoria_id=row['categoria_id']  # Sigues usando `categoria_id`
            )
            producto.categoria_nombre = row['categoria_nombre']
            productos.append(producto)
    conexion.close()
    return productos


# Realiza una búsqueda avanzada con múltiples filtros
def busqueda_avanzada(query=None, categoria_id=None, precio_min=None, precio_max=None):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categoria_id, p.imagen
        FROM productos p
        WHERE 1=1
        """
        params = []
        
        if query:
            sql += " AND (p.nombre LIKE %s OR p.descripcion LIKE %s)"
            params.extend(['%' + query + '%', '%' + query + '%'])
        
        if categoria_id:
            sql += " AND p.categoria_id = %s"
            params.append(categoria_id)
        
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
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categoria_id, p.imagen
        FROM productos p
        JOIN productos original ON p.categoria_id = original.categoria_id
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
def obtener_opiniones(producto_id):
    conexion = obtener_conexion()
    opiniones = []
    with conexion.cursor(DictCursor) as cursor:
        cursor.execute("""
        SELECT o.id, o.calificacion, o.comentario, o.fecha, u.nombre, u.apellido
        FROM opiniones o
        JOIN usuarios u ON o.usuario_id = u.id
        WHERE o.producto_id = %s
        ORDER BY o.fecha DESC
        """, (producto_id,))
        opiniones = cursor.fetchall()
    conexion.close()
    return opiniones

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

def obtener_productos_visitados_recientes(usuario_id, limite=6):
    conexion = obtener_conexion()
    productos_visitados = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT id, nombre, precio 
        FROM productos
        WHERE id IN (
            SELECT producto_id 
            FROM productos_visitados 
            WHERE usuario_id = %s
        )
        ORDER BY fecha_visita DESC
        LIMIT %s
        """
        cursor.execute(sql, (usuario_id, limite))
        productos_visitados = cursor.fetchall()
    conexion.close()
    # Devolver como una lista de diccionarios
    return [
        {'id': row[0], 'nombre': row[1], 'precio': row[2]}
        for row in productos_visitados
    ]


def actualizar_stock(producto_id, cantidad):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_select = "SELECT stock FROM productos WHERE id = %s"
            cursor.execute(sql_select, (producto_id,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                raise ValueError(f"No se encontró el producto con ID {producto_id}")
            
            stock_actual = resultado[0]
            nuevo_stock = stock_actual + cantidad
            
            if nuevo_stock < 0:
                raise ValueError(f"Stock insuficiente para el producto con ID {producto_id}")
            
            sql_update = "UPDATE productos SET stock = %s WHERE id = %s"
            cursor.execute(sql_update, (nuevo_stock, producto_id))
        
        conexion.commit()
        print(f"Stock actualizado para el producto {producto_id}. Nuevo stock: {nuevo_stock}")
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar el stock: {str(e)}")
        raise e
    finally:
        conexion.close()

def obtener_rango_precios():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT MIN(precio) as precio_min, MAX(precio) as precio_max
            FROM productos
            WHERE precio > 0
            """
            cursor.execute(sql)
            resultado = cursor.fetchone()
            
            if resultado:
                precio_min = float(resultado['precio_min']) if resultado['precio_min'] is not None else 0
                precio_max = float(resultado['precio_max']) if resultado['precio_max'] is not None else 0
                return precio_min, precio_max
            else:
                return 0, 0
    finally:
        conexion.close()

def obtener_productos_destacados(limite=4):
    conexion = obtener_conexion()
    productos = []  # Inicializamos como una lista
    with conexion.cursor(DictCursor) as cursor:
        # Intentamos obtener productos que estén marcados como destacados
        sql = """
        SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen
        FROM productos
        WHERE destacado = 1
        LIMIT %s
        """
        cursor.execute(sql, (limite,))
        productos = list(cursor.fetchall())  # Nos aseguramos de que 'productos' sea una lista

        # Si no hay suficientes productos destacados, obtenemos productos aleatorios
        if len(productos) < limite:
            sql = """
            SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen
            FROM productos
            ORDER BY RAND()
            LIMIT %s
            """
            cursor.execute(sql, (limite - len(productos),))
            productos_aleatorios = list(cursor.fetchall())  # Aseguramos que 'productos_aleatorios' sea una lista
            productos.extend(productos_aleatorios)  # Extendemos la lista de productos con productos aleatorios
    
    conexion.close()
    return productos

