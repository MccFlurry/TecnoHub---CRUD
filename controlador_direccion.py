from bd import obtener_conexion

def insertar_direccion_envio(idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO DireccionEnvio(idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3))
    conexion.commit()
    conexion.close()

def obtener_direcciones_envio():
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT idDireccion, idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3 
        FROM DireccionEnvio
        """
        cursor.execute(sql)
        direcciones = cursor.fetchall()
    conexion.close()
    return direcciones

def eliminar_direccion_envio(idDireccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM DireccionEnvio WHERE idDireccion = %s", (idDireccion,))
    conexion.commit()
    conexion.close()

def obtener_direccion_envio_por_id(idDireccion):
    conexion = obtener_conexion()
    direccion = None
    with conexion.cursor() as cursor:
        sql = """
        SELECT idDireccion, idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3 
        FROM DireccionEnvio WHERE idDireccion = %s
        """
        cursor.execute(sql, (idDireccion,))
        direccion = cursor.fetchone()
    conexion.close()
    return direccion

def actualizar_direccion_envio(idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3, idDireccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = """
        UPDATE DireccionEnvio 
        SET idUsuario = %s, direccion = %s, codigoPostal = %s, referencia = %s, idPais = %s, idDivision1 = %s, idDivision2 = %s, idDivision3 = %s 
        WHERE idDireccion = %s
        """
        cursor.execute(sql, (idUsuario, direccion, codigoPostal, referencia, idPais, idDivision1, idDivision2, idDivision3, idDireccion))
    conexion.commit()
    conexion.close()