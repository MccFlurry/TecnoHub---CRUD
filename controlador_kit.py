from bd import obtener_conexion

def insertar_kit(nombre, idUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Kit (nombre, idUsuario) VALUES (%s, %s)", (nombre, idUsuario))
    conexion.commit()
    conexion.close()

def obtener_kits():
    conexion = obtener_conexion()
    kits = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Kit")
        kits = cursor.fetchall()
    conexion.close()
    return kits

def eliminar_kit(idKit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Kit WHERE idKit = %s", (idKit,))
    conexion.commit()
    conexion.close()

def obtener_kit_por_id(idKit):
    conexion = obtener_conexion()
    kit = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Kit WHERE idKit = %s", (idKit,))
        kit = cursor.fetchone()
    conexion.close()
    return kit

def actualizar_kit(nombre, idUsuario, idKit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Kit SET nombre = %s, idUsuario = %s WHERE idKit = %s", (nombre, idUsuario, idKit))
    conexion.commit()
    conexion.close()
