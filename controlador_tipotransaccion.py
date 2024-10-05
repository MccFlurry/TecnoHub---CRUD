from bd import obtener_conexion

def insertar_detalle_transaccion(idTransaccion, idProducto, cantidad, precio_unitario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Detalle_Transaccion (idTransaccion, idProducto, cantidad, precio_unitario) 
            VALUES (%s, %s, %s, %s)
            """, (idTransaccion, idProducto, cantidad, precio_unitario))
    conexion.commit()
    conexion.close()

def obtener_detalles_transaccion():
    conexion = obtener_conexion()
    detalles = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Transaccion")
        detalles = cursor.fetchall()
    conexion.close()
    return detalles

def eliminar_detalle_transaccion(idDetalleTransaccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Detalle_Transaccion WHERE idDetalleTransaccion = %s", (idDetalleTransaccion,))
    conexion.commit()
    conexion.close()

def obtener_detalle_transaccion_por_id(idDetalleTransaccion):
    conexion = obtener_conexion()
    detalle = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Transaccion WHERE idDetalleTransaccion = %s", (idDetalleTransaccion,))
        detalle = cursor.fetchone()
    conexion.close()
    return detalle

def actualizar_detalle_transaccion(idTransaccion, idProducto, cantidad, precio_unitario, idDetalleTransaccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Detalle_Transaccion 
            SET idTransaccion = %s, idProducto = %s, cantidad = %s, precio_unitario = %s 
            WHERE idDetalleTransaccion = %s
            """, (idTransaccion, idProducto, cantidad, precio_unitario, idDetalleTransaccion))
    conexion.commit()
    conexion.close()
