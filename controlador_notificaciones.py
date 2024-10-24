from bd import obtener_conexion
import pymysql.cursors
from clase.clase_notificaciones import Notificaciones

def agregar_notificacion(usuario_id, mensaje):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO notificaciones (usuario_id, mensaje) VALUES (%s, %s)"
            cursor.execute(sql, (usuario_id, mensaje))
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

def obtener_notificaciones_usuario(usuario_id):
    conexion = obtener_conexion()
    notificaciones = []
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, usuario_id, mensaje, fecha_creacion, visto FROM notificaciones WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            for row in rows:
                notificaciones.append(Notificaciones(**row))
    except Exception as e:
        print(f"Error al obtener notificaciones del usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return notificaciones

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

def obtener_notificaciones_no_vistas():
    conexion = obtener_conexion()
    notificaciones = []
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT n.id, n.usuario_id, n.mensaje, n.fecha_creacion, n.visto, u.nombre AS usuario_nombre
            FROM notificaciones n
            JOIN usuarios u ON n.usuario_id = u.id
            WHERE n.visto = 0
            ORDER BY n.fecha_creacion DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                notificaciones.append(Notificaciones(**row))
    except Exception as e:
        print(f"Error al obtener notificaciones no vistas: {e}")
    finally:
        conexion.close()
    return notificaciones

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