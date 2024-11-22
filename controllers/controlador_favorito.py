from bd import obtener_conexion
from clase.clase_favorito import Favorito
import pymysql.cursors

def agregar_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO favoritos (usuario_id, producto_id) VALUES (%s, %s)"
            cursor.execute(sql, (usuario_id, producto_id))
        conexion.commit()
    except Exception as e:
        print(f"Error al agregar favorito: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def eliminar_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
            cursor.execute(sql, (usuario_id, producto_id))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar favorito: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_favoritos_usuario(usuario_id):
    conexion = obtener_conexion()
    favoritos = []
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id, usuario_id, producto_id FROM favoritos WHERE usuario_id = %s"
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            for row in rows:
                favoritos.append(Favorito(**row))
    except Exception as e:
        print(f"Error al obtener favoritos del usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return favoritos

def existe_favorito(usuario_id, producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT COUNT(*) FROM favoritos WHERE usuario_id = %s AND producto_id = %s"
            cursor.execute(sql, (usuario_id, producto_id))
            result = cursor.fetchone()
    except Exception as e:
        print(f"Error al verificar existencia del favorito: {e}")
        result = [0]  # Retornar 0 en caso de error para indicar que no existe el favorito
    finally:
        conexion.close()
    return result[0] > 0