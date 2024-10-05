from bd import obtener_conexion

def insertar_comprobante(tipoComprobante, fecha, hora, isna, total, subTotal, idUsuario, idTransaccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Comprobante (tipoComprobante, fecha, hora, isna, total, subTotal, idUsuario, idTransaccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (tipoComprobante, fecha, hora, isna, total, subTotal, idUsuario, idTransaccion))
    conexion.commit()
    conexion.close()

def obtener_comprobantes():
    conexion = obtener_conexion()
    comprobantes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Comprobante")
        comprobantes = cursor.fetchall()
    conexion.close()
    return comprobantes

def eliminar_comprobante(idComprobante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Comprobante WHERE idComprobante = %s", (idComprobante,))
    conexion.commit()
    conexion.close()

def obtener_comprobante_por_id(idComprobante):
    conexion = obtener_conexion()
    comprobante = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Comprobante WHERE idComprobante = %s", (idComprobante,))
        comprobante = cursor.fetchone()
    conexion.close()
    return comprobante

def actualizar_comprobante(tipoComprobante, fecha, hora, isna, total, subTotal, idUsuario, idTransaccion, idComprobante):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Comprobante 
            SET tipoComprobante = %s, fecha = %s, hora = %s, isna = %s, total = %s, subTotal = %s, 
            idUsuario = %s, idTransaccion = %s 
            WHERE idComprobante = %s
            """, (tipoComprobante, fecha, hora, isna, total, subTotal, idUsuario, idTransaccion, idComprobante))
    conexion.commit()
    conexion.close()
