from bd import obtener_conexion

def insertar_detalle_comprobante(idComprobante, idProducto, precio_unitario, monto, cantidad):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Detalle_Comprobante (idComprobante, idProducto, precio_unitario, monto, cantidad) 
            VALUES (%s, %s, %s, %s, %s)
            """, (idComprobante, idProducto, precio_unitario, monto, cantidad))
    conexion.commit()
    conexion.close()

def obtener_detalles_comprobante():
    conexion = obtener_conexion()
    detalles = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Comprobante")
        detalles = cursor.fetchall()
    conexion.close()
    return detalles

def eliminar_detalle_comprobante(idDetalleComprobante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Detalle_Comprobante WHERE idDetalleComprobante = %s", (idDetalleComprobante,))
    conexion.commit()
    conexion.close()

def obtener_detalle_comprobante_por_id(idDetalleComprobante):
    conexion = obtener_conexion()
    detalle = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Comprobante WHERE idDetalleComprobante = %s", (idDetalleComprobante,))
        detalle = cursor.fetchone()
    conexion.close()
    return detalle

def actualizar_detalle_comprobante(idComprobante, idProducto, precio_unitario, monto, cantidad, idDetalleComprobante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Detalle_Comprobante 
            SET idComprobante = %s, idProducto = %s, precio_unitario = %s, monto = %s, cantidad = %s 
            WHERE idDetalleComprobante = %s
            """, (idComprobante, idProducto, precio_unitario, monto, cantidad, idDetalleComprobante))
    conexion.commit()
    conexion.close()
