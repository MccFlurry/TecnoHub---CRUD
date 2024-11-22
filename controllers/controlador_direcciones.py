from bd import obtener_conexion
from clase.clase_direcciones import Direcciones
from pymysql.err import IntegrityError
import requests
import logging
from datetime import datetime, timedelta
import json
from . import controlador_ubicacion

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def geocodificar_direccion(direccion_completa):
    """
    Geocodifica una dirección usando el caché o la API de Google Maps
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Buscar en caché
            sql = """
                SELECT latitud, longitud 
                FROM geocoding_cache 
                WHERE direccion_completa = %s 
                AND fecha_expiracion > NOW() 
                AND activo = true
            """
            cursor.execute(sql, (direccion_completa,))
            cached = cursor.fetchone()
            
            if cached:
                return {'latitud': cached[0], 'longitud': cached[1]}

            # Si no está en caché, consultar API
            api_key = "TU_API_KEY"  # Reemplazar con tu API key
            response = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json',
                params={
                    'address': direccion_completa,
                    'key': api_key
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    location = data['results'][0]['geometry']['location']
                    
                    # Guardar en caché
                    sql = """
                        INSERT INTO geocoding_cache 
                        (direccion_completa, latitud, longitud, datos_api, fecha_expiracion)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        direccion_completa,
                        location['lat'],
                        location['lng'],
                        json.dumps(data),
                        datetime.now() + timedelta(days=30)
                    ))
                    conexion.commit()
                    return {'latitud': location['lat'], 'longitud': location['lng']}
            return None
    except Exception as e:
        logger.error(f"Error en geocodificación: {str(e)}")
        return None
    finally:
        conexion.close()

def agregar_direccion(usuario_id, direccion, ciudad_id, estado_id, pais_id, codigo_postal, distrito_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            logger.info(f"Agregando dirección para usuario_id: {usuario_id}")

            # Validar usuario
            validation_sql = "SELECT 1 FROM usuarios WHERE id = %s"
            cursor.execute(validation_sql, (usuario_id,))
            if not cursor.fetchone():
                raise ValueError(f"Usuario con ID {usuario_id} no existe.")

            # Obtener nombres de ubicaciones
            ciudad_data = controlador_ubicacion.obtener_ciudad_por_id(ciudad_id)
            estado_data = controlador_ubicacion.obtener_estado_por_id(estado_id)
            pais_data = controlador_ubicacion.obtener_pais_por_id(pais_id)
            distrito_data = controlador_ubicacion.obtener_distrito_por_id(distrito_id)

            if not all([ciudad_data, estado_data, pais_data, distrito_data]):
                raise ValueError("No se encontraron todos los datos de ubicación")

            ciudad_nombre = ciudad_data['nombre']
            estado_nombre = estado_data['nombre']
            pais_nombre = pais_data['nombre']
            distrito_nombre = distrito_data['nombre']

            # Geocodificar dirección
            direccion_completa = f"{direccion}, {distrito_nombre}, {ciudad_nombre}, {estado_nombre}, {pais_nombre}"
            coordenadas = geocodificar_direccion(direccion_completa)

            # SQL para insertar dirección (solo con distrito_id)
            sql = """
            INSERT INTO direcciones (
                usuario_id, direccion, ciudad, estado, pais, 
                codigo_postal, latitud, longitud, direccion_completa,
                distrito_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario_id, direccion, ciudad_nombre, estado_nombre, pais_nombre, 
                codigo_postal,
                coordenadas['latitud'] if coordenadas else None,
                coordenadas['longitud'] if coordenadas else None,
                direccion_completa,
                distrito_id
            ))
            
            conexion.commit()
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Error al agregar dirección: {str(e)}")
        conexion.rollback()
        raise
    finally:
        conexion.close()

def obtener_direcciones_usuario(usuario_id):
    conexion = obtener_conexion()
    direcciones = []
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT 
                d.id, d.usuario_id, d.direccion, d.ciudad, d.estado, d.pais, 
                d.codigo_postal, d.latitud, d.longitud, d.direccion_completa,
                d.direccion_predeterminada, d.distrito_id, di.nombre as distrito_nombre
            FROM direcciones d
            LEFT JOIN distritos di ON di.id = d.distrito_id
            WHERE d.usuario_id = %s
            ORDER BY d.direccion_predeterminada DESC, d.id DESC
            """
            cursor.execute(sql, (usuario_id,))
            for row in cursor.fetchall():
                direcciones.append({
                    'id': row[0],
                    'usuario_id': row[1],
                    'direccion': row[2],
                    'ciudad': row[3],
                    'estado': row[4],
                    'pais': row[5],
                    'codigo_postal': row[6],
                    'latitud': float(row[7]) if row[7] else None,
                    'longitud': float(row[8]) if row[8] else None,
                    'direccion_completa': row[9],
                    'direccion_predeterminada': bool(row[10]),
                    'distrito_id': row[11],
                    'distrito': row[12]  # Nombre del distrito obtenido del JOIN
                })
    except Exception as e:
        logger.error(f"Error al obtener direcciones del usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return direcciones

def actualizar_direccion(id, datos):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            logger.info(f"Actualizando dirección ID: {id}")

            # Validar y obtener datos de ubicación
            ciudad_data = controlador_ubicacion.obtener_ciudad_por_id(datos['ciudad_id'])
            estado_data = controlador_ubicacion.obtener_estado_por_id(datos['estado_id'])
            pais_data = controlador_ubicacion.obtener_pais_por_id(datos['pais_id'])
            distrito_data = controlador_ubicacion.obtener_distrito_por_id(datos['distrito_id'])

            if not all([ciudad_data, estado_data, pais_data, distrito_data]):
                raise ValueError("No se encontraron todos los datos de ubicación")

            ciudad_nombre = ciudad_data['nombre']
            estado_nombre = estado_data['nombre']
            pais_nombre = pais_data['nombre']
            distrito_nombre = distrito_data['nombre']

            # Construir dirección completa
            direccion_completa = f"{datos['direccion']}, {distrito_nombre}, {ciudad_nombre}, {estado_nombre}, {pais_nombre}"

            # Obtener coordenadas
            coordenadas = geocodificar_direccion(direccion_completa)

            sql = """
            UPDATE direcciones SET
                direccion = %s,
                ciudad = %s,
                estado = %s,
                pais = %s,
                codigo_postal = %s,
                latitud = %s,
                longitud = %s,
                direccion_completa = %s,
                distrito_id = %s
            WHERE id = %s
            """
            cursor.execute(sql, (
                datos['direccion'],
                ciudad_nombre,
                estado_nombre,
                pais_nombre,
                datos['codigo_postal'],
                coordenadas['latitud'] if coordenadas else None,
                coordenadas['longitud'] if coordenadas else None,
                direccion_completa,
                datos['distrito_id'],
                id
            ))
            
            conexion.commit()
            return True
    except Exception as e:
        logger.error(f"Error al actualizar dirección: {str(e)}")
        conexion.rollback()
        raise
    finally:
        conexion.close()

def obtener_direccion_por_id(direccion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT d.*, 
                   c.id as ciudad_id, 
                   e.id as estado_id, 
                   p.id as pais_id,
                   d.distrito_id,
                   di.nombre as distrito_nombre
            FROM direcciones d
            LEFT JOIN ciudades c ON c.nombre = d.ciudad
            LEFT JOIN estados e ON e.nombre = d.estado
            LEFT JOIN paises p ON p.nombre = d.pais
            LEFT JOIN distritos di ON di.id = d.distrito_id
            WHERE d.id = %s
            """
            cursor.execute(sql, (direccion_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'usuario_id': row[1],
                    'direccion': row[2],
                    'ciudad': row[3],
                    'estado': row[4],
                    'pais': row[5],
                    'codigo_postal': row[6],
                    'latitud': float(row[7]) if row[7] else None,
                    'longitud': float(row[8]) if row[8] else None,
                    'direccion_completa': row[9],
                    'ciudad_id': row[11],
                    'estado_id': row[12],
                    'pais_id': row[13],
                    'distrito_id': row[14] if row[14] else None,
                    'distrito': row[15] if row[15] else None
                }
            return None
    except Exception as e:
        logger.error(f"Error al obtener dirección por ID {direccion_id}: {str(e)}")
        return None
    finally:
        conexion.close()

def eliminar_direccion(usuario_id, direccion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar pertenencia y uso en pedidos
            sql_verificar = """
                SELECT d.id 
                FROM direcciones d
                LEFT JOIN pedidos p ON d.id = p.direccion_id
                WHERE d.id = %s AND d.usuario_id = %s
            """
            cursor.execute(sql_verificar, (direccion_id, usuario_id))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValueError("La dirección no existe o no te pertenece.")

            sql_eliminar = "DELETE FROM direcciones WHERE id = %s AND usuario_id = %s"
            cursor.execute(sql_eliminar, (direccion_id, usuario_id))
            conexion.commit()
            logger.info(f"Dirección {direccion_id} eliminada con éxito.")
            return True
    except IntegrityError:
        logger.error("No se puede eliminar la dirección porque está asociada a pedidos.")
        conexion.rollback()
        return False
    except Exception as e:
        logger.error(f"Error al eliminar dirección: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()

def establecer_direccion_predeterminada(usuario_id, direccion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Primero verificar que la dirección existe y pertenece al usuario
            sql_verificar = """
                SELECT id FROM direcciones 
                WHERE id = %s AND usuario_id = %s
            """
            cursor.execute(sql_verificar, (direccion_id, usuario_id))
            if not cursor.fetchone():
                raise ValueError("La dirección no existe o no pertenece al usuario")

            # Desactivar todas las direcciones predeterminadas del usuario
            sql_reset = """
                UPDATE direcciones 
                SET direccion_predeterminada = false 
                WHERE usuario_id = %s
            """
            cursor.execute(sql_reset, (usuario_id,))

            # Establecer la nueva dirección predeterminada
            sql_update = """
                UPDATE direcciones 
                SET direccion_predeterminada = true 
                WHERE id = %s
            """
            cursor.execute(sql_update, (direccion_id,))
            
            conexion.commit()
            logger.info(f"Dirección {direccion_id} establecida como predeterminada")
            return True
    except Exception as e:
        logger.error(f"Error al establecer dirección predeterminada: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()