from bd import obtener_conexion
import pymysql.cursors
from clase.clase_notificaciones import Notificaciones
from datetime import datetime

def agregar_notificacion(usuario_id, pedido_id, mensaje):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO notificaciones (usuario_id, pedido_id, mensaje) VALUES (%s, %s, %s)"
            cursor.execute(sql, (usuario_id, pedido_id, mensaje))
        conexion.commit()
    except Exception as e:
        print(f"Error al agregar notificación: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def eliminar_notificacion(notificacion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM notificaciones WHERE id = %s"
            cursor.execute(sql, (notificacion_id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar notificación: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def marcar_notificacion_como_vista(notificacion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE notificaciones SET visto = 1 WHERE id = %s"
            cursor.execute(sql, (notificacion_id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al marcar notificación como vista: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_notificaciones():
    conexion = obtener_conexion()
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT n.id, n.usuario_id, n.mensaje, n.fecha_creacion, n.visto, 
                   u.nombre AS usuario_nombre, u.foto AS usuario_foto
            FROM notificaciones n
            JOIN usuarios u ON n.usuario_id = u.id
            WHERE n.visto = 0
            ORDER BY n.fecha_creacion DESC
            LIMIT 5  # Limitamos a las 5 notificaciones más recientes
            """
            cursor.execute(sql)
            notificaciones = cursor.fetchall()
            
            # Formatear las fechas y serializar los datos
            for notificacion in notificaciones:
                if isinstance(notificacion['fecha_creacion'], datetime):
                    notificacion['fecha_creacion'] = notificacion['fecha_creacion'].strftime('%Y-%m-%d %H:%M:%S')
            
            return notificaciones
            
    except Exception as e:
        print(f"Error al obtener notificaciones no vistas: {e}")
        return []
    finally:
        conexion.close()

def marcar_notificacion_como_vista(notificacion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_verify = "SELECT id FROM notificaciones WHERE id = %s AND visto = 0"
            cursor.execute(sql_verify, (notificacion_id,))
            if not cursor.fetchone():
                return False
            
            sql_update = "UPDATE notificaciones SET visto = 1 WHERE id = %s"
            cursor.execute(sql_update, (notificacion_id,))
            conexion.commit()
            return cursor.rowcount > 0
            
    except Exception as e:
        print(f"Error al marcar notificación como vista: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.close()