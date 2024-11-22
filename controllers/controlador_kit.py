from bd import obtener_conexion
from clase.clase_kit import Kit
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor

def crear_kit(usuario_id, celular_id, smartwatch_id, accesorios_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO kits (usuario_id, celular_id, smartwatch_id, accesorios_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario_id, celular_id, smartwatch_id, accesorios_id))
        conexion.commit()
    except Exception as e:
        print(f"Error al crear kit: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_kits_usuario(usuario_id):
    conexion = obtener_conexion()
    kits = []
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT k.id, k.usuario_id, k.celular_id, k.smartwatch_id, k.accesorios_id, k.fecha_creacion,
                   c.nombre as celular_nombre, c.precio as celular_precio,
                   f.nombre as smartwatch_nombre, f.precio as smartwatch_precio,
                   a.nombre as accesorios_nombre, a.precio as accesorios_precio
            FROM kits k
            JOIN productos c ON k.celular_id = c.id
            JOIN productos f ON k.smartwatch_id = f.id
            JOIN productos a ON k.accesorios_id = a.id
            WHERE k.usuario_id = %s
            ORDER BY k.fecha_creacion DESC
            """
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            for row in rows:
                kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['smartwatch_id'], row['accesorios_id'], row['fecha_creacion'])
                kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
                kit.smartwatch = Producto(row['smartwatch_id'], row['smartwatch_nombre'], '', row['smartwatch_precio'], 0, 0, '')
                kit.accesorios = Producto(row['accesorios_id'], row['accesorios_nombre'], '', row['accesorios_precio'], 0, 0, '')
                kits.append(kit)
    except Exception as e:
        print(f"Error al obtener kits del usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return kits

def eliminar_kit(kit_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM kits WHERE id = %s"
            cursor.execute(sql, (kit_id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar el kit con id {kit_id}: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_kit_por_id(kit_id):
    conexion = obtener_conexion()
    kit = None
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT k.id, k.usuario_id, k.celular_id, k.smartwatch_id, k.accesorios_id, k.fecha_creacion,
                   c.nombre as celular_nombre, c.precio as celular_precio,
                   f.nombre as smartwatch_nombre, f.precio as smartwatch_precio,
                   a.nombre as accesorios_nombre, a.precio as accesorios_precio
            FROM kits k
            JOIN productos c ON k.celular_id = c.id
            JOIN productos f ON k.smartwatch_id = f.id
            JOIN productos a ON k.accesorios_id = a.id
            WHERE k.id = %s
            """
            cursor.execute(sql, (kit_id,))
            row = cursor.fetchone()
            if row:
                kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['smartwatch_id'], row['accesorios_id'], row['fecha_creacion'])
                kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
                kit.smartwatch = Producto(row['smartwatch_id'], row['smartwatch_nombre'], '', row['smartwatch_precio'], 0, 0, '')
                kit.accesorios = Producto(row['accesorios_id'], row['accesorios_nombre'], '', row['accesorios_precio'], 0, 0, '')
    except Exception as e:
        print(f"Error al obtener el kit con id {kit_id}: {e}")
    finally:
        conexion.close()
    return kit