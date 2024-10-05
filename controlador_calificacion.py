from bd import obtener_conexion

def insertar_calificacion(puntuacion, opinion, fecha, hora, idUsuario, idProducto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Calificacion (puntuacion, opinion, fecha, hora, idUsuario, idProducto) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (puntuacion, opinion, fecha, hora, idUsuario, idProducto))
    conexion.commit()
    conexion.close()

def obtener_calificaciones():
    conexion = obtener_conexion()
    calificaciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Calificacion")
        calificaciones = cursor.fetchall()
    conexion.close()
    return calificaciones

def eliminar_calificacion(idCalificacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Calificacion WHERE idCalificacion = %s", (idCalificacion,))
    conexion.commit()
    conexion.close()

def obtener_calificacion_por_id(idCalificacion):
    conexion = obtener_conexion()
    calificacion = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Calificacion WHERE idCalificacion = %s", (idCalificacion,))
        calificacion = cursor.fetchone()
    conexion.close()
    return calificacion

def actualizar_calificacion(puntuacion, opinion, fecha, hora, idUsuario, idProducto, idCalificacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Calificacion 
            SET puntuacion = %s, opinion = %s, fecha = %s, hora = %s, idUsuario = %s, idProducto = %s 
            WHERE idCalificacion = %s
            """, (puntuacion, opinion, fecha, hora, idUsuario, idProducto, idCalificacion))
    conexion.commit()
    conexion.close()
