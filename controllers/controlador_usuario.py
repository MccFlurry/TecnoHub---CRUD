from clase.clase_usuario import Usuario
from bd import obtener_conexion
from datetime import datetime
import bcrypt
import pymysql.cursors
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def insertar_usuario(nombre, apellido, email, contrasena, tipo, foto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            hashed_password = hash_password(contrasena)
            sql = "INSERT INTO usuarios(nombre, apellido, email, contrasena, tipo, foto) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, apellido, email, hashed_password, tipo, foto))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False
    finally:
        conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, tipo, foto, fecha_registro, contrasena FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(**row)
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
    finally:
        conexion.close()
    return usuario

def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, contrasena, tipo, foto, fecha_registro FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(**row)
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
    finally:
        conexion.close()
    return usuario

def actualizar_usuario(id, nombre, apellido, email, tipo, foto=None, nueva_contrasena=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            if nueva_contrasena:
                hashed_password = hash_password(nueva_contrasena)
                sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s, contrasena = %s WHERE id = %s"
                cursor.execute(sql, (nombre, apellido, email, tipo, foto, hashed_password, id))
            else:
                sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s WHERE id = %s"
                cursor.execute(sql, (nombre, apellido, email, tipo, foto, id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False
    finally:
        conexion.close()

def eliminar_usuario(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        conexion.close()

def contar_usuarios():
    conexion = obtener_conexion()
    total_usuarios = 0
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT COUNT(*) as total FROM usuarios"
            cursor.execute(sql)
            total_usuarios = cursor.fetchone()['total']
    except Exception as e:
        print(f"Error al contar usuarios: {e}")
    finally:
        conexion.close()
    return total_usuarios

def obtener_todos_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, tipo, foto, contrasena, fecha_registro FROM usuarios"
            cursor.execute(sql)
            rows = cursor.fetchall()
            usuarios = [Usuario(**row) for row in rows]
    except Exception as e:
        print(f"Error al obtener todos los usuarios: {e}")
    finally:
        conexion.close()
    return usuarios

def tiene_pedidos_pendientes(usuario_id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            SELECT COUNT(*) 
            FROM pedidos 
            WHERE usuario_id = %s 
            AND estado IN ('pendiente', 'en_proceso', 'enviado')
            """
            cursor.execute(sql, (usuario_id,))
            cantidad = cursor.fetchone()[0]
            return cantidad > 0
    except Exception as e:
        logger.error(f"Error al verificar pedidos pendientes del usuario {usuario_id}: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def iniciar_sesion(email, password):
    usuario = obtener_usuario_por_email(email)
    if usuario and check_password(usuario.contrasena, password):
        return {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'tipo': usuario.tipo,
            'foto': usuario.foto
        }
    return None

def generar_reporte_actividad(periodo='7d'):
    """
    Genera un reporte de actividad de usuarios basado en un periodo específico.
    
    :param periodo: Periodo de actividad ('7d', '30d', '90d')
    :return: Lista de diccionarios con actividad de usuarios
    """
    conexion = obtener_conexion()
    reporte = []
    
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            # Consulta para obtener actividad de usuarios en el periodo especificado
            sql = """
            SELECT 
                u.id, 
                u.nombre, 
                u.email, 
                COUNT(DISTINCT p.id) as total_pedidos,
                MAX(p.fecha) as ultimo_pedido,
                COUNT(DISTINCT o.id) as total_opiniones
            FROM 
                usuarios u
            LEFT JOIN 
                pedidos p ON u.id = p.usuario_id AND p.fecha >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            LEFT JOIN 
                opiniones o ON u.id = o.usuario_id AND o.fecha >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY 
                u.id, u.nombre, u.email
            HAVING 
                total_pedidos > 0 OR total_opiniones > 0
            ORDER BY 
                total_pedidos DESC, total_opiniones DESC
            """
            
            # Mapeo de periodos a días
            periodo_dias = {
                '7d': 7,
                '30d': 30,
                '90d': 90
            }
            
            # Obtener días para el periodo, default 7 días
            dias = periodo_dias.get(periodo, 7)
            
            cursor.execute(sql, (dias, dias))
            
            # Convertir resultados a lista de diccionarios
            reporte = cursor.fetchall()
            
            # Registrar el reporte generado
            logging.info(f"Reporte de actividad de usuarios generado para periodo {periodo}")
            
    except Exception as e:
        logging.error(f"Error al generar reporte de actividad de usuarios: {e}")
        reporte = []
    
    finally:
        conexion.close()
    
    return reporte

def generar_reporte_registros(periodo):
    """
    Genera un reporte de registros de usuarios en un período específico
    
    Args:
        periodo (str): Período de tiempo ('7d', '30d', '90d', '1y')
        
    Returns:
        dict: Reporte con estadísticas de registros
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            # Convertir período a días
            dias = {
                '7d': 7,
                '30d': 30,
                '90d': 90,
                '1y': 365
            }.get(periodo, 30)
            
            sql = """
            SELECT 
                COUNT(*) as total_registros,
                DATE(fecha_registro) as fecha,
                DAYNAME(fecha_registro) as dia_semana
            FROM usuarios
            WHERE fecha_registro >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY DATE(fecha_registro), DAYNAME(fecha_registro)
            ORDER BY DATE(fecha_registro)
            """
            cursor.execute(sql, (dias,))
            registros_diarios = cursor.fetchall()
            
            # Calcular estadísticas
            total_registros = sum(r['total_registros'] for r in registros_diarios)
            promedio_diario = total_registros / len(registros_diarios) if registros_diarios else 0
            
            return {
                'periodo': periodo,
                'total_registros': total_registros,
                'promedio_diario': round(promedio_diario, 2),
                'registros_por_dia': [{
                    'fecha': r['fecha'].strftime('%Y-%m-%d'),
                    'dia_semana': r['dia_semana'],
                    'registros': r['total_registros']
                } for r in registros_diarios]
            }
            
    except Exception as e:
        print(f"Error al generar reporte de registros: {str(e)}")
        raise Exception(f"Error al generar reporte de registros: {str(e)}")
    finally:
        conexion.close()

def obtener_top_compradores(limite=10):
    """
    Obtiene los usuarios que más han comprado
    
    Args:
        limite (int): Cantidad de usuarios a retornar
        
    Returns:
        list: Lista de usuarios con sus estadísticas de compra
    """
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT 
                u.id,
                u.nombre,
                COUNT(DISTINCT p.id) as total_pedidos,
                COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) as total_compras
            FROM usuarios u
            LEFT JOIN pedidos p ON u.id = p.usuario_id
            LEFT JOIN detalles_pedido dp ON p.id = dp.pedido_id
            WHERE p.estado = 'completado'
            GROUP BY u.id, u.nombre
            ORDER BY total_compras DESC
            LIMIT %s
            """
            cursor.execute(sql, (int(limite),))
            compradores = cursor.fetchall()
            
            return [{
                'id': c['id'],
                'nombre': c['nombre'],
                'total_pedidos': c['total_pedidos'],
                'total_compras': float(c['total_compras'])
            } for c in compradores]
            
    except Exception as e:
        print(f"Error al obtener top compradores: {str(e)}")
        raise Exception(f"Error al obtener top compradores: {str(e)}")
    finally:
        conexion.close()