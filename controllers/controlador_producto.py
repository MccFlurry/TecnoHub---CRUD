from bd import obtener_conexion
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor
import logging
import time
import os
from functools import wraps
from datetime import datetime

# Configuración de logging
def setup_logging():
    """Configura el sistema de logging para el manejo de stock"""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'stock_{datetime.now().strftime("%Y%m")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def retry_on_error(max_attempts=3, initial_delay=0.1, max_delay=2.0, backoff_factor=2):
    """
    Decorador para reintentar operaciones con backoff exponencial
    
    Args:
        max_attempts (int): Número máximo de intentos
        initial_delay (float): Retraso inicial entre intentos en segundos
        max_delay (float): Retraso máximo entre intentos en segundos
        backoff_factor (float): Factor de incremento del retraso
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            delay = initial_delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = min(delay, max_delay)
                        logger.warning(
                            f"Intento {attempt + 1} fallido para {func.__name__}. "
                            f"Reintentando en {sleep_time:.2f}s. Error: {str(e)}"
                        )
                        time.sleep(sleep_time)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"Todos los intentos fallidos para {func.__name__}. "
                            f"Error final: {str(e)}"
                        )
            
            raise last_exception
        return wrapper
    return decorator

class StockError(Exception):
    """Clase base para errores relacionados con el stock"""
    pass

class StockInsuficienteError(StockError):
    """Error que indica que no hay suficiente stock"""
    pass

class ProductoNoEncontradoError(StockError):
    """Error que indica que el producto no existe"""
    pass

@retry_on_error(max_attempts=3, initial_delay=0.1, max_delay=2.0)
def actualizar_stock(id_producto, cantidad, conexion=None, timeout=10):
    """
    Actualiza el stock de un producto de manera segura y concurrente
    
    Args:
        id_producto (int): ID del producto a actualizar
        cantidad (int): Cantidad a reducir del stock
        conexion (Connection, optional): Conexión a la base de datos
        timeout (int): Tiempo máximo de espera para la transacción en segundos
    
    Returns:
        bool: True si la actualización fue exitosa
    
    Raises:
        ValueError: Si los parámetros son inválidos
        StockInsuficienteError: Si no hay suficiente stock
        ProductoNoEncontradoError: Si el producto no existe
        Exception: Para otros errores inesperados
    """
    # Validación de parámetros
    if not isinstance(id_producto, int) or id_producto <= 0:
        raise ValueError(f"ID de producto inválido: {id_producto}")
    
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError(f"Cantidad inválida: {cantidad}")

    start_time = time.time()
    close_connection = False

    try:
        # Obtener conexión si no se proporcionó una
        if conexion is None:
            conexion = obtener_conexion()
            close_connection = True

        with conexion.cursor() as cursor:
            # Configurar timeout y nivel de aislamiento
            cursor.execute(f"SET SESSION innodb_lock_wait_timeout = {timeout}")
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            conexion.begin()

            # Verificar y bloquear el producto
            cursor.execute("""
                SELECT stock 
                FROM productos 
                WHERE id = %s 
                FOR UPDATE
            """, (id_producto,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ProductoNoEncontradoError(f"Producto {id_producto} no encontrado")

            stock_actual = resultado[0] or 0
            
            # Verificar stock suficiente
            if stock_actual < cantidad:
                raise StockInsuficienteError(
                    f"Stock insuficiente para producto {id_producto}. "
                    f"Disponible: {stock_actual}, Solicitado: {cantidad}"
                )

            # Verificar timeout
            if time.time() - start_time > timeout:
                logger.warning(f"Timeout alcanzado para producto {id_producto}")
                conexion.rollback()
                return False

            # Actualizar stock
            cursor.execute("""
                UPDATE productos 
                SET stock = stock - %s
                WHERE id = %s
            """, (cantidad, id_producto))

            if cursor.rowcount != 1:
                raise Exception(f"Error al actualizar stock del producto {id_producto}")

            # Registrar actualización exitosa
            logger.info(
                f"Stock actualizado exitosamente - "
                f"Producto: {id_producto}, "
                f"Cantidad: -{cantidad}, "
                f"Stock restante: {stock_actual - cantidad}"
            )

            conexion.commit()
            return True

    except StockError as e:
        # Errores esperados de negocio
        if conexion:
            conexion.rollback()
        logger.warning(str(e))
        raise

    except Exception as e:
        # Errores inesperados
        if conexion:
            conexion.rollback()
        logger.error(f"Error crítico actualizando stock: {str(e)}")
        raise

    finally:
        if close_connection and conexion:
            conexion.close()

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