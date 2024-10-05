from bd import obtener_conexion

def insertar(idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Trabajador(idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais))
    conexion.commit()
    conexion.close()


def obtener():
    conexion = obtener_conexion()
    trabajadores = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT idTrabajador, idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais
            FROM Trabajador""")
        trabajadores = cursor.fetchall()
    conexion.close()
    return trabajadores


def eliminar(idTrabajador):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Trabajador WHERE idTrabajador = %s", (idTrabajador,))
    conexion.commit()
    conexion.close()


def obtener_por_id(idTrabajador):
    conexion = obtener_conexion()
    trabajador = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT idTrabajador, idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais
            FROM Trabajador WHERE idTrabajador = %s""", (idTrabajador,))
        trabajador = cursor.fetchone()
    conexion.close()
    return trabajador


def actualizar(idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais, idTrabajador):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Trabajador
            SET idUsuario = %s, numero_documento = %s, tipo_documento = %s, fecha_nacimiento = %s, fecha_ingreso = %s, sexo = %s, cargo = %s, vigencia = %s, idPais = %s
            WHERE idTrabajador = %s""", (idUsuario, numero_documento, tipo_documento, fecha_nacimiento, fecha_ingreso, sexo, cargo, vigencia, idPais, idTrabajador))
    conexion.commit()
    conexion.close()
