from bd import obtener_conexion
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def insertar_producto(nombre, descripcion, categoria_id, precio, stock, destacado, imagen):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO productos (nombre, descripcion, categoria_id, precio, stock, destacado, imagen)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, descripcion, categoria_id, precio, stock, destacado, imagen))
        conexion.commit()
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al insertar producto: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_producto_por_id(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen, categoria_id FROM productos WHERE id = %s", (id,))
            producto = cursor.fetchone()
            
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
    except Exception as e:
        logger.error(f"Error al obtener producto por ID: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_por_categorias(categoria_id):
    conexion = None
    try:
        conexion = obtener_conexion()
        productos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen FROM productos WHERE categoria_id = %s"
            cursor.execute(sql, (categoria_id,))
            rows = cursor.fetchall()
            for row in rows:
                productos.append(Producto(**row))
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos por categoría: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_por_ids(ids):
    conexion = None
    try:
        conexion = obtener_conexion()
        productos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, descripcion, precio, stock, imagen, categoria_id FROM productos WHERE id IN ({})".format(
                ', '.join(['%s'] * len(ids))
            )
            cursor.execute(sql, ids)
            rows = cursor.fetchall()
            for row in rows:
                productos.append(Producto(**row))
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos por IDs: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def actualizar_producto(id, nombre, descripcion, precio, stock, categoria_id, imagen):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            UPDATE productos 
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria_id = %s, imagen = %s 
            WHERE id = %s
            """
            cursor.execute(sql, (nombre, descripcion, precio, stock, categoria_id, imagen, id))
        conexion.commit()
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al actualizar producto: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def eliminar_producto(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "DELETE FROM productos WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al eliminar producto: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def buscar_productos(query):
    conexion = None
    try:
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
        return productos
    except Exception as e:
        logger.error(f"Error al buscar productos: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_relacionados(producto_id, limite=4):
    conexion = None
    try:
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
                productos.append(Producto(**row))
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos relacionados: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_todos_productos():
    conexion = None
    try:
        conexion = obtener_conexion()
        productos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.imagen, p.categoria_id, c.nombre AS categoria_nombre
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id ASC
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
                    categoria_id=row['categoria_id']
                )
                producto.categoria_nombre = row['categoria_nombre']
                productos.append(producto)
        return productos
    except Exception as e:
        logger.error(f"Error al obtener todos los productos: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def busqueda_avanzada(query=None, categoria_id=None, precio_min=None, precio_max=None):
    conexion = None
    try:
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
        return productos
    except Exception as e:
        logger.error(f"Error en búsqueda avanzada: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_recomendados(producto_id, limite=4):
    conexion = None
    try:
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
            productos = cursor.fetchall()
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos recomendados: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def contar_productos():
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM productos"
            cursor.execute(sql)
            total_productos = cursor.fetchone()[0]
        return total_productos
    except Exception as e:
        logger.error(f"Error al contar productos: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_visitados_recientes(usuario_id, limite=6):
    conexion = None
    try:
        conexion = obtener_conexion()
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
        return [
            {'id': row[0], 'nombre': row[1], 'precio': row[2]}
            for row in productos_visitados
        ]
    except Exception as e:
        logger.error(f"Error al obtener productos visitados recientes: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def actualizar_stock(producto_id, cantidad):
    conexion = None
    try:
        conexion = obtener_conexion()
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
        logger.info(f"Stock actualizado para el producto {producto_id}. Nuevo stock: {nuevo_stock}")
        return nuevo_stock
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al actualizar el stock: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_rango_precios():
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor(DictCursor) as cursor:
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
            return 0, 0
    except Exception as e:
        logger.error(f"Error al obtener rango de precios: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_productos_destacados(limite=4):
    conexion = None
    try:
        conexion = obtener_conexion()
        productos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen
            FROM productos
            WHERE destacado = 1
            LIMIT %s
            """
            cursor.execute(sql, (limite,))
            productos = list(cursor.fetchall())

            if len(productos) < limite:
                sql = """
                SELECT id, nombre, descripcion, precio, stock, categoria_id, imagen
                FROM productos
                ORDER BY RAND()
                LIMIT %s
                """
                cursor.execute(sql, (limite - len(productos),))
                productos_aleatorios = list(cursor.fetchall())
                productos.extend(productos_aleatorios)
        
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos destacados: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()