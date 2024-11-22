from bd import obtener_conexion
from clase.clase_categorias import categorias
from pymysql.cursors import DictCursor
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def obtener_todas_categorias():
    conexion = None
    try:
        conexion = obtener_conexion()
        categorias = []
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre FROM categorias ORDER BY id ASC"
            cursor.execute(sql)
            categorias = cursor.fetchall()
        return categorias
    except Exception as e:
        logger.error(f"Error al obtener todas las categorías: {str(e)}")
        return []
    finally:
        if conexion:
            conexion.close()

def obtener_categorias_por_id(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre FROM categorias WHERE id = %s"
            cursor.execute(sql, (id,))
            categoria = cursor.fetchone()
            return categoria if categoria else None
    except Exception as e:
        logger.error(f"Error al obtener la categoría con id {id}: {str(e)}")
        return None
    finally:
        if conexion:
            conexion.close()

def insertar_categorias(nombre):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor(DictCursor) as cursor:
            sql = "INSERT INTO categorias(nombre) VALUES (%s)"
            cursor.execute(sql, (nombre,))
        conexion.commit()
        return True
    except Exception as e:
        logger.error(f"Error al insertar categoría: {str(e)}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()

def actualizar_categorias(id, nombre):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor(DictCursor) as cursor:
            sql = "UPDATE categorias SET nombre = %s WHERE id = %s"
            cursor.execute(sql, (nombre, id))
        conexion.commit()
        return True
    except Exception as e:
        logger.error(f"Error al actualizar la categoría con id {id}: {str(e)}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()

def eliminar_categorias(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor(DictCursor) as cursor:
            # Primero verificamos si hay productos asociados
            sql_check = "SELECT COUNT(*) as count FROM productos WHERE categoria_id = %s"
            cursor.execute(sql_check, (id,))
            result = cursor.fetchone()
            if result and result['count'] > 0:
                raise Exception("No se puede eliminar la categoría porque tiene productos asociados")
            
            # Si no hay productos asociados, procedemos con la eliminación
            sql = "DELETE FROM categorias WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
        return True
    except Exception as e:
        logger.error(f"Error al eliminar la categoría con id {id}: {str(e)}")
        if conexion:
            conexion.rollback()
        return False
    finally:
        if conexion:
            conexion.close()

def contar_productos_por_categoria(categoria_id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM productos WHERE categoria_id = %s"
            cursor.execute(sql, (categoria_id,))
            return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error al contar productos de la categoría {categoria_id}: {str(e)}")
        return 0
    finally:
        if conexion:
            conexion.close()