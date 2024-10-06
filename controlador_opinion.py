from bd import obtener_conexion
from clase.clase_opinion import Opinion

def agregar_opinion(producto_id, usuario_id, comentario, calificacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO opiniones (producto_id, usuario_id, comentario, calificacion) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (producto_id, usuario_id, comentario, calificacion))
    conexion.commit()
    conexion.close()

def obtener_opiniones_producto(producto_id):
    conexion = obtener_conexion()
    opiniones = []
    with conexion.cursor() as cursor:
        sql = """
        SELECT o.id, o.producto_id, o.usuario_id, o.comentario, o.calificacion, o.fecha, u.nombre, u.apellido
        FROM opiniones o
        JOIN usuarios u ON o.usuario_id = u.id
        WHERE o.producto_id = %s
        ORDER BY o.fecha DESC
        """
        cursor.execute(sql, (producto_id,))
        rows = cursor.fetchall()
        for row in rows:
            opinion = Opinion(row['id'], row['producto_id'], row['usuario_id'], row['comentario'], row['calificacion'], row['fecha'])
            opinion.nombre_usuario = f"{row['nombre']} {row['apellido']}"
            opiniones.append(opinion)
    conexion.close()
    return opiniones

def calcular_calificacion_promedio(producto_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "SELECT AVG(calificacion) as promedio FROM opiniones WHERE producto_id = %s"
        cursor.execute(sql, (producto_id,))
        resultado = cursor.fetchone()
    conexion.close()
    return resultado['promedio'] if resultado['promedio'] else 0