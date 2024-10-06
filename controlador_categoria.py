from bd import obtener_conexion
from clase.clase_categoria import Categoria

def obtener_todas_categorias():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre FROM categorias"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            categorias.append(Categoria(**row))
    conexion.close()
    return categorias

def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        sql = "SELECT id, nombre FROM categorias WHERE id = %s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            categoria = Categoria(**row)
    conexion.close()
    return categoria

def insertar_categoria(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO categorias(nombre) VALUES (%s)"
        cursor.execute(sql, (nombre,))
    conexion.commit()
    conexion.close()

def actualizar_categoria(id, nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE categorias SET nombre = %s WHERE id = %s"
        cursor.execute(sql, (nombre, id))
    conexion.commit()
    conexion.close()

def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM categorias WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

