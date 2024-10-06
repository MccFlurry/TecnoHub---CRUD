from bd import obtener_conexion
from clase.clase_direcciones import Direcciones

def agregar_direccion(usuario_id, direccion, ciudad, estado, pais, codigo_postal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO direcciones (usuario_id, direccion, ciudad, estado, pais, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (usuario_id, direccion, ciudad, estado, pais, codigo_postal))
    conexion.commit()
    conexion.close()

def obtener_direcciones_usuario(usuario_id):
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, usuario_id, direccion, ciudad, estado, pais, codigo_postal FROM direcciones WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            direcciones.append(Direccion(**row))
    conexion.close()
    return direcciones

def actualizar_direccion(id, direccion, ciudad, estado, pais, codigo_postal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE direcciones SET direccion = %s, ciudad = %s, estado = %s, pais = %s, codigo_postal = %s WHERE id = %s"
        cursor.execute(sql, (direccion, ciudad, estado, pais, codigo_postal, id))
    conexion.commit()
    conexion.close()

def eliminar_direccion(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM direcciones WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()