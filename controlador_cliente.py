from bd import obtener_conexion

def insertar(idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Cliente(idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais)
            VALUES (%s, %s, %s, %s, %s)""", (idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais))
    conexion.commit()
    conexion.close()


def obtener():
    conexion = obtener_conexion()
    clientes = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT idCliente, idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais FROM Cliente""")
        clientes = cursor.fetchall()
    conexion.close()
    return clientes


def eliminar(idCliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Cliente WHERE idCliente = %s", (idCliente,))
    conexion.commit()
    conexion.close()


def obtener_por_id(idCliente):
    conexion = obtener_conexion()
    cliente = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT idCliente, idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais
            FROM Cliente WHERE idCliente = %s""", (idCliente,))
        cliente = cursor.fetchone()
    conexion.close()
    return cliente


def actualizar(idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais, idCliente):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE Cliente
            SET idUsuario = %s, fecha_nacimiento = %s, tipo_documento = %s, numero_documento = %s, idPais = %s
            WHERE idCliente = %s""", (idUsuario, fecha_nacimiento, tipo_documento, numero_documento, idPais, idCliente))
    conexion.commit()
    conexion.close()
