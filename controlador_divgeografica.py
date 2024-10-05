from bd import obtener_conexion

def insertar_division_geografica(nombre, nivel, idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO Division_Geografica(nombre, nivel, idPais) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, nivel, idPais))
    conexion.commit()
    conexion.close()

def obtener_divisiones_geograficas():
    conexion = obtener_conexion()
    divisiones = []
    with conexion.cursor() as cursor:
        sql = "SELECT idDivision, nombre, nivel, idPais FROM Division_Geografica"
        cursor.execute(sql)
        divisiones = cursor.fetchall()
    conexion.close()
    return divisiones

def eliminar_division_geografica(idDivision):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Division_Geografica WHERE idDivision = %s", (idDivision,))
    conexion.commit()
    conexion.close()

def obtener_division_geografica_por_id(idDivision):
    conexion = obtener_conexion()
    division = None
    with conexion.cursor() as cursor:
        sql = "SELECT idDivision, nombre, nivel, idPais FROM Division_Geografica WHERE idDivision = %s"
        cursor.execute(sql, (idDivision,))
        division = cursor.fetchone()
    conexion.close()
    return division

def actualizar_division_geografica(nombre, nivel, idPais, idDivision):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE Division_Geografica SET nombre = %s, nivel = %s, idPais = %s WHERE idDivision = %s"
        cursor.execute(sql, (nombre, nivel, idPais, idDivision))
    conexion.commit()
    conexion.close()