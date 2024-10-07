from bd import obtener_conexion
from clase.clase_categorias import categorias
from pymysql.cursors import DictCursor

def obtener_todas_categorias():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre FROM categorias"
        cursor.execute(sql)
        categorias = cursor.fetchall()
    conexion.close()
    return categorias

def obtener_categorias_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre FROM categorias WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                categoria = {
                    'id': row['id'],
                    'nombre': row['nombre']
                }
    except Exception as e:
        print(f"Error al obtener la categoría con id {id}: {e}")
    finally:
        conexion.close()
    
    return categoria

def insertar_categorias(nombre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "INSERT INTO categorias(nombre) VALUES (%s)"
            cursor.execute(sql, (nombre,))
        conexion.commit()
    except Exception as e:
        print(f"Error al insertar categoría: {e}")
    finally:
        conexion.close()

def actualizar_categorias(id, nombre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "UPDATE categorias SET nombre = %s WHERE id = %s"
            cursor.execute(sql, (nombre, id))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar la categoría con id {id}: {e}")
    finally:
        conexion.close()

def eliminar_categorias(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "DELETE FROM categorias WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar la categoría con id {id}: {e}")
    finally:
        conexion.close()