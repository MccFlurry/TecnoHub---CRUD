from bd import obtener_conexion

def insertar_transaccion(tipoTransaccion, cantidad, estado, metodo_pago, total, subTotal, fechaTransaccion, horaTransaccion, idUsuario, idDireccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Transaccion (tipoTransaccion, cantidad, estado, metodo_pago, total, subTotal, fechaTransaccion, horaTransaccion, idUsuario, idDireccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (tipoTransaccion, cantidad, estado, metodo_pago, total, subTotal, fechaTransaccion, horaTransaccion, idUsuario, idDireccion))
    conexion.commit()
    conexion.close()

def obtener_transacciones():
    conexion = obtener_conexion()
    transacciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Transaccion")
        transacciones = cursor.fetchall()
    conexion.close()
    return transacciones

def eliminar_transaccion(idTransaccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Transaccion WHERE idTransaccion = %s", (idTransaccion,))
    conexion.commit()
    conexion.close()

def obtener_transaccion_por_id(idTransaccion):
    conexion = obtener_conexion()
    transaccion = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Transaccion WHERE idTransaccion = %s", (idTransaccion,))
        transaccion = cursor.fetchone()
    conexion.close()
    return transaccion

def actualizar_transaccion(tipoTransaccion, cantidad, estado, metodo_pago, total, subTotal, fechaTransaccion, horaTransaccion, idUsuario, idDireccion, idTransaccion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Transaccion 
            SET tipoTransaccion = %s, cantidad = %s, estado = %s, metodo_pago = %s, total = %s, subTotal = %s, 
            fechaTransaccion = %s, horaTransaccion = %s, idUsuario = %s, idDireccion = %s 
            WHERE idTransaccion = %s
            """, (tipoTransaccion, cantidad, estado, metodo_pago, total, subTotal, fechaTransaccion, horaTransaccion, idUsuario, idDireccion, idTransaccion))
    conexion.commit()
    conexion.close()
