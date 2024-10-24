from bd import obtener_conexion
import pymysql.cursors
from clase.clase_notificaciones import Notificaciones

def agregar_notificacion(usuario_id, mensaje):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO notificaciones (usuario_id, mensaje) VALUES (%s, %s)"
        cursor.execute(sql, (usuario_id, mensaje))
    conexion.commit()
    conexion.close()

def eliminar_notificacion(notificacion_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM notificaciones WHERE id = %s"
        cursor.execute(sql, (notificacion_id,))
    conexion.commit()
    conexion.close()

def obtener_notificaciones_usuario(usuario_id):
    conexion = obtener_conexion()
    notificaciones = []
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT id, usuario_id, mensaje, fecha_creacion, visto FROM notificaciones WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            notificaciones.append(Notificaciones(**row))
    conexion.close()
    return notificaciones

def marcar_notificacion_como_vista(notificacion_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE notificaciones SET visto = 1 WHERE id = %s"
        cursor.execute(sql, (notificacion_id,))
    conexion.commit()
    conexion.close()

def obtener_notificaciones_no_vistas():
    conexion = obtener_conexion()
    notificaciones = []
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
    conexion.close()
    return notificaciones

def marcar_notificacion_como_vista(notificacion_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE notificaciones SET visto = 1 WHERE id = %s"
        cursor.execute(sql, (notificacion_id,))
    conexion.commit()
    conexion.close()
