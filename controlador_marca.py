from bd import obtener_conexion
from clase.clase_marca import Marca

def insertar_marca(marca):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO marcas (nombre) VALUES (%s)",
                         (marca.nombre,))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise Exception(f"Error al insertar la marca: {str(e)}")
    finally:
        conexion.close()

def obtener_marca_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre FROM marcas WHERE id = %s", (id,))
        fila = cursor.fetchone()
        if fila:
            marca = Marca(nombre=fila[1], id=fila[0])
    conexion.close()
    return marca

def obtener_marcas():
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM marcas")
        filas = cursor.fetchall()
        for fila in filas:
            marca = Marca(nombre=fila[1], id=fila[0])
            marcas.append(marca)
    conexion.close()
    return marcas

def eliminar_marca(id):
    conexion = obtener_conexion()
    try:
        # Primero verificamos si hay productos asociados
        cantidad_productos = contar_productos_por_marca(id)
        if cantidad_productos > 0:
            raise Exception("Esta marca esta asociada a un producto")
            
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM marcas WHERE id = %s", (id,))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

def actualizar_marca(marca):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE marcas SET nombre = %s WHERE id = %s",
                      (marca.nombre, marca.id))
    conexion.commit()
    conexion.close()

def contar_productos_por_marca(id_marca):
    conexion = obtener_conexion()
    cantidad = 0
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM productos WHERE id_marca = %s", (id_marca,))
        fila = cursor.fetchone()
        if fila:
            cantidad = fila[0]
    conexion.close()
    return cantidad
