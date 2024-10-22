from bd import obtener_conexion
import pymysql.cursors

class Notificacion:
    def __init__(self, id, usuario_id, mensaje, fecha_creacion, visto):
        self.id = id
        self.usuario_id = usuario_id
        self.mensaje = mensaje
        self.fecha_creacion = fecha_creacion
        self.visto = visto

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
            notificaciones.append(Notificacion(**row))
    conexion.close()
    return notificaciones

def obtener_notificaciones_no_vistas():
    conexion = obtener_conexion()
    notificaciones = []
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT id, usuario_id, mensaje, fecha_creacion, visto FROM notificaciones WHERE visto = 0"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            notificaciones.append(Notificacion(**row))
    conexion.close()
    return notificaciones

def marcar_notificacion_como_vista(notificacion_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE notificaciones SET visto = 1 WHERE id = %s"
        cursor.execute(sql, (notificacion_id,))
    conexion.commit()
    conexion.close()
