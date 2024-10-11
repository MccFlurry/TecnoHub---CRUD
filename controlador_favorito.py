from bd import obtener_conexion
from clase.clase_favorito import Favorito
import pymysql.cursors

def agregar_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO favoritos (usuario_id, producto_id) VALUES (%s, %s)"
        cursor.execute(sql, (usuario_id, producto_id))
    conexion.commit()
    conexion.close()

def eliminar_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        cursor.execute(sql, (usuario_id, producto_id))
    conexion.commit()
    conexion.close()

def obtener_favoritos_usuario(usuario_id):
    conexion = obtener_conexion()
    favoritos = []
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT id, usuario_id, producto_id FROM favoritos WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            favoritos.append(Favorito(**row))
    conexion.close()
    return favoritos

def existe_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
        cursor.execute(sql, (usuario_id, producto_id))
        result = cursor.fetchone()
    conexion.close()
    return result[0] > 0 