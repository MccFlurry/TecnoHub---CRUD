from bd import obtener_conexion

def insertar_pais(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Pais (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()

def obtener_paises():
    conexion = obtener_conexion()
    paises = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Pais")
        paises = cursor.fetchall()
    conexion.close()
    return paises

def eliminar_pais(idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Pais WHERE idPais = %s", (idPais,))
    conexion.commit()
    conexion.close()

def obtener_pais_por_id(idPais):
    conexion = obtener_conexion()
    pais = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Pais WHERE idPais = %s", (idPais,))
        pais = cursor.fetchone()
    conexion.close()
    return pais

def actualizar_pais(nombre, idPais):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Pais SET nombre = %s WHERE idPais = %s", (nombre, idPais))
    conexion.commit()
    conexion.close()
