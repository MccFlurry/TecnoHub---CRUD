from bd import obtener_conexion
from clase.clase_modelo import Modelo

def insertar_modelo(modelo):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO modelos (nombre) VALUES (%s)",
                         (modelo.nombre,))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise Exception(f"Error al insertar el modelo: {str(e)}")
    finally:
        conexion.close()

def obtener_modelo_por_id(id):
    conexion = obtener_conexion()
    modelo = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre FROM modelos WHERE id = %s", (id,))
        fila = cursor.fetchone()
        if fila:
            modelo = Modelo(nombre=fila[1], id=fila[0])
    conexion.close()
    return modelo

def obtener_modelos():
    conexion = obtener_conexion()
    modelos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM modelos")
        filas = cursor.fetchall()
        for fila in filas:
            modelo = Modelo(nombre=fila[1], id=fila[0])
            modelos.append(modelo)
    conexion.close()
    return modelos

def eliminar_modelo(id):
    conexion = obtener_conexion()
    try:
        # Primero verificamos si hay productos asociados
        cantidad_productos = contar_productos_por_modelo(id)
        if cantidad_productos > 0:
            raise Exception("Este modelo esta asociado a un producto")
            
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM modelos WHERE id = %s", (id,))
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        conexion.close()

def actualizar_modelo(modelo):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE modelos SET nombre = %s WHERE id = %s",
                      (modelo.nombre, modelo.id))
    conexion.commit()
    conexion.close()

def contar_productos_por_modelo(id_modelo):
    conexion = obtener_conexion()
    cantidad = 0
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM productos WHERE id_modelo = %s", (id_modelo,))
        fila = cursor.fetchone()
        if fila:
            cantidad = fila[0]
    conexion.close()
    return cantidad
