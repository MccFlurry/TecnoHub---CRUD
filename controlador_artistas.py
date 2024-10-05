from bd import obtener_conexion

def insertar_artista(nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO artista(nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream))
    conexion.commit()
    conexion.close()

def obtener_artista():
    conexion = obtener_conexion()
    artistas = []
    with conexion.cursor() as cursor:
        sql = "SELECT id,nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream FROM artista"
        cursor.execute(sql)
        artistas = cursor.fetchall()
    conexion.close()
    return artistas

def eliminar_artista(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM artista WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_artista_por_id(id):
    conexion = obtener_conexion()
    artista = None
    with conexion.cursor() as cursor:
        sql = "SELECT id,nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream FROM artista WHERE id = %s"
        cursor.execute(sql, (id))
        juego = cursor.fetchone()
    conexion.close()
    return juego


def actualizar_artista(nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE artista SET  nombre = %s, nacionalidad = %s, aniolanzamiento = %s, cantidaddiscos = %s, web = %s, redsocialprincipal = %s, promediostream = %s WHERE id = %s"
        cursor.execute(sql,(nombre,nacionalidad,aniolanzamiento,cantidaddiscos,web,redsocialprincipal,promediostream,id))
    conexion.commit()
    conexion.close()



