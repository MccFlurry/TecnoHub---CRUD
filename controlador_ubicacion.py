from bd import obtener_conexion
from clase.clase_pais import Pais
from clase.clase_estado import Estado
from clase.clase_ciudad import Ciudad
from clase.clase_distrito import Distrito
import logging

logger = logging.getLogger(__name__)

def obtener_todos_paises():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, nombre, codigo_iso 
            FROM paises 
            WHERE activo = true 
            ORDER BY nombre
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'codigo_iso': row[2]
                } for row in resultados
            ]
    except Exception as e:
        logger.error(f"Error al obtener países: {str(e)}")
        return []
    finally:
        conexion.close()

def obtener_estados_por_pais(pais_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, nombre, codigo 
            FROM estados 
            WHERE pais_id = %s AND activo = true 
            ORDER BY nombre
            """
            cursor.execute(sql, (pais_id,))
            resultados = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'codigo': row[2]
                } for row in resultados
            ]
    except Exception as e:
        logger.error(f"Error al obtener estados: {str(e)}")
        return []
    finally:
        conexion.close()

def obtener_ciudades_por_estado(estado_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, nombre, codigo_postal_patron
            FROM ciudades 
            WHERE estado_id = %s AND activo = true 
            ORDER BY nombre
            """
            cursor.execute(sql, (estado_id,))
            resultados = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'codigo_postal_patron': row[2]
                } for row in resultados
            ]
    except Exception as e:
        logger.error(f"Error al obtener ciudades: {str(e)}")
        return []
    finally:
        conexion.close()

def obtener_distritos_por_ciudad(ciudad_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, nombre
            FROM distritos 
            WHERE ciudad_id = %s AND activo = true 
            ORDER BY nombre
            """
            cursor.execute(sql, (ciudad_id,))
            resultados = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'nombre': row[1]
                } for row in resultados
            ]
    except Exception as e:
        logger.error(f"Error al obtener distritos: {str(e)}")
        return []
    finally:
        conexion.close()

def obtener_pais_por_id(pais_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, nombre, codigo_iso
            FROM paises 
            WHERE id = %s AND activo = true
            """
            cursor.execute(sql, (pais_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'nombre': row[1],
                    'codigo_iso': row[2]
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener país: {str(e)}")
        return None
    finally:
        conexion.close()

def obtener_estado_por_id(estado_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, pais_id, nombre, codigo
            FROM estados 
            WHERE id = %s AND activo = true
            """
            cursor.execute(sql, (estado_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'pais_id': row[1],
                    'nombre': row[2],
                    'codigo': row[3]
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener estado: {str(e)}")
        return None
    finally:
        conexion.close()

def obtener_ciudad_por_id(ciudad_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, estado_id, nombre, codigo_postal_patron
            FROM ciudades 
            WHERE id = %s AND activo = true
            """
            cursor.execute(sql, (ciudad_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'estado_id': row[1],
                    'nombre': row[2],
                    'codigo_postal_patron': row[3]
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener ciudad: {str(e)}")
        return None
    finally:
        conexion.close()

def obtener_distrito_por_id(distrito_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, ciudad_id, nombre
            FROM distritos 
            WHERE id = %s AND activo = true
            """
            cursor.execute(sql, (distrito_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'ciudad_id': row[1],
                    'nombre': row[2]
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener distrito: {str(e)}")
        return None
    finally:
        conexion.close()

def obtener_ubicacion_completa(distrito_id):
    """
    Obtiene toda la información jerárquica de ubicación para un distrito
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT 
                d.id as distrito_id,
                d.nombre as distrito_nombre,
                c.id as ciudad_id,
                c.nombre as ciudad_nombre,
                c.codigo_postal_patron,
                e.id as estado_id,
                e.nombre as estado_nombre,
                e.codigo as estado_codigo,
                p.id as pais_id,
                p.nombre as pais_nombre,
                p.codigo_iso as pais_codigo
            FROM distritos d
            JOIN ciudades c ON d.ciudad_id = c.id
            JOIN estados e ON c.estado_id = e.id
            JOIN paises p ON e.pais_id = p.id
            WHERE d.id = %s AND d.activo = true
            """
            cursor.execute(sql, (distrito_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'distrito': {
                        'id': row[0],
                        'nombre': row[1]
                    },
                    'ciudad': {
                        'id': row[2],
                        'nombre': row[3],
                        'codigo_postal_patron': row[4]
                    },
                    'estado': {
                        'id': row[5],
                        'nombre': row[6],
                        'codigo': row[7]
                    },
                    'pais': {
                        'id': row[8],
                        'nombre': row[9],
                        'codigo_iso': row[10]
                    }
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener ubicación completa: {str(e)}")
        return None
    finally:
        conexion.close()