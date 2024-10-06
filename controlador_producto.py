from bd import obtener_conexion
from clase.clase_producto import Producto                                               

def insertar_producto(nombre, descripcion, precio, stock, categoria_id, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO productos(nombre, descripcion, precio, stock, categoria_id, imagen) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, precio, stock, categoria_id, imagen))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos WHERE id = %s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            producto = Producto(**row)
    conexion.close()
    return producto

def obtener_productos_por_categoria(categoria_id):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos WHERE categoria_id = %s"
        cursor.execute(sql, (categoria_id,))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))
    conexion.close()
    return productos

def actualizar_producto(id, nombre, descripcion, precio, stock, categoria_id, imagen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria_id = %s, imagen = %s WHERE id = %s"
        cursor.execute(sql, (nombre, descripcion, precio, stock, categoria_id, imagen, id))
    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

def obtener_productos_destacados(limite=6):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos ORDER BY RAND() LIMIT %s"
        cursor.execute(sql, (limite,))
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))
    conexion.close()
    return productos

def buscar_productos(query):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
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

def obtener_productos_relacionados(producto_id, limite=4):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
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
            productos.append(Producto(**row))
    conexion.close()
    return productos

def obtener_todos_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            productos.append(Producto(**row))
    conexion.close()
    return productos

def busqueda_avanzada(query, categoria_id, precio_min, precio_max):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
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

def obtener_productos_recomendados(producto_id, limite=4):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
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

def agregar_resena(producto_id, usuario_id, calificacion, comentario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
        INSERT INTO resenas (producto_id, usuario_id, calificacion, comentario)
        VALUES (%s, %s, %s, %s)
        """, (producto_id, usuario_id, calificacion, comentario))
    conexion.commit()
    conexion.close()

def obtener_resenas(producto_id):
    conexion = obtener_conexion()
    resenas = []
    with conexion.cursor() as cursor:
        cursor.execute("""
        SELECT r.id, r.calificacion, r.comentario, r.fecha, u.nombre, u.apellido
        FROM resenas r
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.producto_id = %s
        ORDER BY r.fecha DESC
        """, (producto_id,))
        resenas = cursor.fetchall()
    conexion.close()
    return resenas

def calcular_calificacion_promedio(producto_id):
    conexion = obtener_conexion()
    promedio = 0
    with conexion.cursor() as cursor:
        cursor.execute("""
        SELECT AVG(calificacion) as promedio
        FROM resenas
        WHERE producto_id = %s
        """, (producto_id,))
        resultado = cursor.fetchone()
        if resultado and resultado['promedio']:
            promedio = round(resultado['promedio'], 1)
    conexion.close()
    return promedio