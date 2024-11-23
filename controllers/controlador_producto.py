from bd import obtener_conexion
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def insertar_producto(nombre, descripcion, categoria_id, precio, imagen, stock=0, id_marca=None, id_modelo=None):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO productos (nombre, descripcion, categoria_id, precio, imagen, stock, id_marca, id_modelo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Asegurarse de que stock sea un entero y no None
            stock = 0 if stock is None else int(stock)
            cursor.execute(sql, (nombre, descripcion, categoria_id, precio, imagen, stock, id_marca, id_modelo))
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
            sql = """SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.categoria_id, 
                    p.id_marca, p.id_modelo, p.destacado, p.imagen 
                    FROM productos p WHERE p.id = %s"""
            cursor.execute(sql, (id,))
            datos = cursor.fetchone()
            
            if datos is not None:
                producto = Producto(
                    id=datos[0],
                    nombre=datos[1],
                    descripcion=datos[2],
                    precio=datos[3],
                    stock=datos[4],
                    categoria_id=datos[5],
                    id_marca=datos[6],
                    id_modelo=datos[7],
                    destacado=datos[8],
                    imagen=datos[9]
                )
                return producto
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
            sql = "SELECT id, nombre, descripcion, precio, stock, imagen, categoria_id, id_marca, id_modelo FROM productos WHERE categoria_id = %s"
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
            sql = "SELECT id, nombre, descripcion, precio, imagen, categoria_id, id_marca, id_modelo FROM productos WHERE id IN ({})".format(
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

def actualizar_producto(id, nombre, descripcion, precio, categoria_id, imagen, stock=0, id_marca=None, id_modelo=None):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            UPDATE productos 
            SET nombre = %s, descripcion = %s, precio = %s, 
                categoria_id = %s, imagen = %s, stock = %s, id_marca = %s, id_modelo = %s
            WHERE id = %s
            """
            # Asegurarse de que stock sea un entero y no None
            stock = 0 if stock is None else int(stock)
            cursor.execute(sql, (nombre, descripcion, precio, categoria_id, imagen, stock, id_marca, id_modelo, id))
        conexion.commit()
        return True
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al actualizar producto: {str(e)}")
        return False
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
            SELECT id, nombre, descripcion, precio, imagen, categoria_id, id_marca, id_modelo 
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
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.imagen, p.categoria_id, p.id_marca, p.id_modelo 
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
            SELECT p.*, c.nombre as categoria_nombre, 
                   m.nombre as marca_nombre, mo.nombre as modelo_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN marcas m ON p.id_marca = m.id
            LEFT JOIN modelos mo ON p.id_modelo = mo.id
            ORDER BY p.id DESC
            """
            cursor.execute(sql)
            productos_data = cursor.fetchall()
            for producto_data in productos_data:
                producto = Producto(**{k: v for k, v in producto_data.items() if k in Producto.__init__.__code__.co_varnames})
                producto.categoria_nombre = producto_data['categoria_nombre']
                producto.marca_nombre = producto_data['marca_nombre']
                producto.modelo_nombre = producto_data['modelo_nombre']
                productos.append(producto)
        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_todas_marcas():
    conexion = None
    try:
        conexion = obtener_conexion()
        marcas = []
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre FROM marcas ORDER BY nombre"
            cursor.execute(sql)
            marcas = cursor.fetchall()
        return marcas
    except Exception as e:
        logger.error(f"Error al obtener marcas: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_todos_modelos():
    conexion = None
    try:
        conexion = obtener_conexion()
        modelos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, id_marca FROM modelos ORDER BY nombre"
            cursor.execute(sql)
            modelos = cursor.fetchall()
        return modelos
    except Exception as e:
        logger.error(f"Error al obtener modelos: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def busqueda_avanzada(query=None, categoria_id=None, precio_min=None, precio_max=None, id_marca=None, id_modelo=None):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            condiciones = []
            parametros = []
            
            if query:
                condiciones.append("(nombre LIKE %s OR descripcion LIKE %s)")
                parametros.extend([f"%{query}%", f"%{query}%"])
            
            if categoria_id:
                condiciones.append("categoria_id = %s")
                parametros.append(categoria_id)
            
            if precio_min is not None:
                condiciones.append("precio >= %s")
                parametros.append(precio_min)
            
            if precio_max is not None:
                condiciones.append("precio <= %s")
                parametros.append(precio_max)
                
            if id_marca:
                condiciones.append("id_marca = %s")
                parametros.append(id_marca)
                
            if id_modelo:
                condiciones.append("id_modelo = %s")
                parametros.append(id_modelo)
            
            sql = "SELECT id, nombre, descripcion, precio, imagen, categoria_id, id_marca, id_modelo FROM productos"
            
            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones)
            
            cursor.execute(sql, parametros)
            productos = []
            for fila in cursor.fetchall():
                producto = Producto(
                    id=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    precio=fila[3],
                    imagen=fila[4],
                    categoria_id=fila[5],
                    id_marca=fila[6],
                    id_modelo=fila[7]
                )
                productos.append(producto)
            return productos
            
    except Exception as e:
        logger.error(f"Error en búsqueda avanzada: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()
    return []

def obtener_productos_recomendados(producto_id, limite=4):
    conexion = None
    try:
        conexion = obtener_conexion()
        productos = []
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.imagen, p.categoria_id, p.id_marca, p.id_modelo
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
            SELECT id, nombre, descripcion, precio, imagen, categoria_id, id_marca, id_modelo
            FROM productos
            ORDER BY RAND()
            LIMIT %s
            """
            cursor.execute(sql, (limite,))
            productos = list(cursor.fetchall())

        return productos
    except Exception as e:
        logger.error(f"Error al obtener productos destacados: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def actualizar_stock(id_producto, cantidad):
    """
    Actualiza el stock de un producto.
    Args:
        id_producto: ID del producto a actualizar
        cantidad: Cantidad a reducir del stock (positiva o negativa)
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Verificar existencia y stock actual del producto
            sql_verificar = "SELECT stock FROM productos WHERE id = %s"
            cursor.execute(sql_verificar, (id_producto,))
            resultado = cursor.fetchone()
            
            if not resultado:
                logger.error(f"Producto con ID {id_producto} no encontrado")
                return False
                
            stock_actual = resultado[0] if resultado[0] is not None else 0
            
            # Convertir la cantidad a un valor positivo para la reducción
            cantidad_reducir = abs(cantidad)
                
            # Verificar si hay suficiente stock
            if stock_actual < cantidad_reducir:
                logger.error(f"Stock insuficiente para producto {id_producto}. Stock actual: {stock_actual}, Cantidad requerida: {cantidad_reducir}")
                return False
                
            # Actualizar el stock
            nuevo_stock = stock_actual - cantidad_reducir
            sql_actualizar = "UPDATE productos SET stock = %s WHERE id = %s"
            cursor.execute(sql_actualizar, (nuevo_stock, id_producto))
            
            # Registrar el movimiento de stock
            logger.info(f"Stock actualizado para producto {id_producto}: {stock_actual} -> {nuevo_stock}")
            
            conexion.commit()
            return True
            
    except Exception as e:
        if conexion:
            conexion.rollback()
        logger.error(f"Error al actualizar stock: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def obtener_stock(id_producto):
    """
    Obtiene el stock actual de un producto.
    Args:
        id_producto: ID del producto
    Returns:
        int: Cantidad en stock, o None si el producto no existe
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT stock FROM productos WHERE id = %s"
            cursor.execute(sql, (id_producto,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        logger.error(f"Error al obtener stock: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()