from bd import obtener_conexion

def insertar_detalle_kit(idKit, idCategoria, idProducto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Detalle_Kit (idKit, idCategoria, idProducto) 
            VALUES (%s, %s, %s)
            """, (idKit, idCategoria, idProducto))
    conexion.commit()
    conexion.close()

def obtener_detalles_kit():
    conexion = obtener_conexion()
    detalles = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Kit")
        detalles = cursor.fetchall()
    conexion.close()
    return detalles

def eliminar_detalle_kit(idDetalleKit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Detalle_Kit WHERE id_kit_detalle = %s", (idDetalleKit,))
    conexion.commit()
    conexion.close()

def obtener_detalle_kit_por_id(idDetalleKit):
    conexion = obtener_conexion()
    detalle = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM Detalle_Kit WHERE id_kit_detalle = %s", (idDetalleKit,))
        detalle = cursor.fetchone()
    conexion.close()
    return detalle

def actualizar_detalle_kit(idKit, idCategoria, idProducto, idDetalleKit):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE Detalle_Kit 
            SET idKit = %s, idCategoria = %s, idProducto = %s 
            WHERE id_kit_detalle = %s
            """, (idKit, idCategoria, idProducto, idDetalleKit))
    conexion.commit()
    conexion.close()
