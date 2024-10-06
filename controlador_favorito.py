from bd import obtener_conexion
from clase.clase_favorito import Favorito

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
    with conexion.cursor() as cursor:
        sql = "SELECT id, usuario_id, producto_id FROM favoritos WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            favoritos.append(Favorito(**row))
    conexion.close()
    return favoritos