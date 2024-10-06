from bd import obtener_conexion
from clase.clase_kit import Kit
from clase.clase_producto import Producto

def crear_kit(usuario_id, celular_id, funda_id, audifonos_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO kits (usuario_id, celular_id, funda_id, audifonos_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario_id, celular_id, funda_id, audifonos_id))
    conexion.commit()
    conexion.close()

def obtener_kits_usuario(usuario_id):
    conexion = obtener_conexion()
    kits = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, usuario_id, celular_id, funda_id, audifonos_id, fecha_creacion FROM kits WHERE usuario_id = %s"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            kits.append(Kit(**row))
    conexion.close()
    return kits

def eliminar_kit(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM kits WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

def crear_kit(usuario_id, celular_id, funda_id, audifonos_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO kits (usuario_id, celular_id, funda_id, audifonos_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario_id, celular_id, funda_id, audifonos_id))
        kit_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return kit_id

def obtener_kit_por_id(kit_id):
    conexion = obtener_conexion()
    kit = None
    with conexion.cursor() as cursor:
        sql = """
        SELECT k.id, k.usuario_id, k.celular_id, k.funda_id, k.audifonos_id, k.fecha_creacion,
               c.nombre as celular_nombre, c.precio as celular_precio,
               f.nombre as funda_nombre, f.precio as funda_precio,
               a.nombre as audifonos_nombre, a.precio as audifonos_precio
        FROM kits k
        JOIN productos c ON k.celular_id = c.id
        JOIN productos f ON k.funda_id = f.id
        JOIN productos a ON k.audifonos_id = a.id
        WHERE k.id = %s
        """
        cursor.execute(sql, (kit_id,))
        row = cursor.fetchone()
        if row:
            kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['funda_id'], row['audifonos_id'], row['fecha_creacion'])
            kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
            kit.funda = Producto(row['funda_id'], row['funda_nombre'], '', row['funda_precio'], 0, 0, '')
            kit.audifonos = Producto(row['audifonos_id'], row['audifonos_nombre'], '', row['audifonos_precio'], 0, 0, '')
    conexion.close()
    return kit

def obtener_kits_usuario(usuario_id):
    conexion = obtener_conexion()
    kits = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT k.id, k.usuario_id, k.celular_id, k.funda_id, k.audifonos_id, k.fecha_creacion,
               c.nombre as celular_nombre, c.precio as celular_precio,
               f.nombre as funda_nombre, f.precio as funda_precio,
               a.nombre as audifonos_nombre, a.precio as audifonos_precio
        FROM kits k
        JOIN productos c ON k.celular_id = c.id
        JOIN productos f ON k.funda_id = f.id
        JOIN productos a ON k.audifonos_id = a.id
        WHERE k.usuario_id = %s
        ORDER BY k.fecha_creacion DESC
        """
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['funda_id'], row['audifonos_id'], row['fecha_creacion'])
            kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
            kit.funda = Producto(row['funda_id'], row['funda_nombre'], '', row['funda_precio'], 0, 0, '')
            kit.audifonos = Producto(row['audifonos_id'], row['audifonos_nombre'], '', row['audifonos_precio'], 0, 0, '')
            kits.append(kit)
    conexion.close()
    return kits

def eliminar_kit(kit_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM kits WHERE id = %s"
        cursor.execute(sql, (kit_id,))
    conexion.commit()
    conexion.close()