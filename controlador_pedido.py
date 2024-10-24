from bd import obtener_conexion
from clase.clase_pedido import Pedido
from clase.clase_detalle_pedido import DetallePedido
from datetime import datetime, timedelta
import pymysql as MySQLdb
import pymysql
from pymysql.cursors import DictCursor

def crear_pedido(usuario_id, direccion_id):
    conexion = obtener_conexion()
    fecha_pedido = datetime.now()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO pedidos (usuario_id, direccion_id, fecha_pedido, estado) VALUES (%s, %s, %s, 'pendiente')"
            cursor.execute(sql, (usuario_id, direccion_id, fecha_pedido))
            pedido_id = cursor.lastrowid
        conexion.commit()
        return pedido_id
    except MySQLdb.Error as e:
        conexion.rollback()
        print(f"Error al crear el pedido: {str(e)}")
        raise e
    finally:
        conexion.close()

def agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio_unitario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO detalles_pedido(pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (pedido_id, producto_id, cantidad, precio_unitario))
        conexion.commit()
    except MySQLdb.Error as e:
        conexion.rollback()
        print(f"Error al agregar detalle al pedido: {str(e)}")
        raise e
    finally:
        conexion.close()

def obtener_pedidos_por_usuario(usuario_id):
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.usuario_id, u.email, u.nombre, u.apellido, p.fecha_pedido, p.estado, d.direccion, d.ciudad, d.estado AS direccion_estado, d.pais, d.codigo_postal,
               SUM(dp.precio_unitario * dp.cantidad) AS total
        FROM pedidos p
        JOIN direcciones d ON p.direccion_id = d.id
        JOIN detalles_pedido dp ON dp.pedido_id = p.id
        JOIN usuarios u ON p.usuario_id = u.id
        WHERE p.usuario_id = %s
        GROUP BY p.id, p.usuario_id, p.fecha_pedido, p.estado, d.direccion, d.ciudad, d.estado, d.pais, d.codigo_postal, u.email, u.nombre, u.apellido
        """
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            row['direccion'] = {
                'direccion': row['direccion'],
                'ciudad': row['ciudad'],
                'estado': row['direccion_estado'],
                'pais': row['pais'],
                'codigo_postal': row['codigo_postal']  # Incluimos el código postal
            }
            pedidos.append(row)
    conexion.close()
    return pedidos

def obtener_detalles_pedido(pedido_id):
    conexion = obtener_conexion()
    detalles = []
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id, pedido_id, producto_id, cantidad, precio_unitario FROM detalles_pedido WHERE pedido_id = %s"
            cursor.execute(sql, (pedido_id,))
            rows = cursor.fetchall()
            for row in rows:
                detalles.append(DetallePedido(**row))
    finally:
        conexion.close()
    return detalles

def actualizar_estado_pedido(pedido_id, nuevo_estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE pedidos SET estado = %s WHERE id = %s"
            cursor.execute(sql, (nuevo_estado, pedido_id))
        conexion.commit()
    except MySQLdb.Error as e:
        conexion.rollback()
        print(f"Error al actualizar el estado del pedido: {str(e)}")
        raise e
    finally:
        conexion.close()

def obtener_todos_pedidos():
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT p.id, p.usuario_id, p.fecha_pedido, p.estado, SUM(dp.cantidad * dp.precio_unitario) AS total, 
               u.nombre, u.apellido
        FROM pedidos p
        JOIN detalles_pedido dp ON p.id = dp.pedido_id
        JOIN usuarios u ON p.usuario_id = u.id
        GROUP BY p.id
        ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(sql)
        pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def obtener_pedido_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    total = 0
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute("""
                SELECT p.id, p.usuario_id, p.fecha_pedido, p.estado, u.nombre, u.apellido, u.email, d.direccion, d.ciudad, d.estado AS direccion_estado, d.pais, d.codigo_postal
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                JOIN direcciones d ON p.direccion_id = d.id
                WHERE p.id = %s
            """, (id,))
            pedido = cursor.fetchone()

            if pedido:
                cursor.execute("""
                    SELECT dp.producto_id, dp.cantidad, dp.precio_unitario, pr.nombre
                    FROM detalles_pedido dp
                    JOIN productos pr ON dp.producto_id = pr.id
                    WHERE dp.pedido_id = %s
                """, (id,))
                detalles = cursor.fetchall()

                for detalle in detalles:
                    subtotal = detalle['cantidad'] * detalle['precio_unitario']
                    total += subtotal

                pedido['detalles'] = detalles
                pedido['total'] = total
    finally:
        conexion.close()
    
    return pedido

def contar_pedidos_pendientes():
    conexion = obtener_conexion()
    count = 0
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM pedidos WHERE estado = 'pendiente'")
            count = cursor.fetchone()[0]
    finally:
        conexion.close()
    return count

def calcular_ingresos_mes():
    conexion = obtener_conexion()
    ingresos = 0
    try:
        with conexion.cursor() as cursor:
            fecha_inicio = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = (fecha_inicio + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            cursor.execute("""
                SELECT SUM(dp.cantidad * dp.precio_unitario) 
                FROM pedidos p
                JOIN detalles_pedido dp ON p.id = dp.pedido_id
                WHERE p.fecha_pedido BETWEEN %s AND %s AND p.estado != 'cancelado'
            """, (fecha_inicio, fecha_fin))
            ingresos = cursor.fetchone()[0] or 0
    finally:
        conexion.close()
    return ingresos

def eliminar_pedido(pedido_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_check_details = "SELECT COUNT(*) FROM detalles_pedido WHERE pedido_id = %s"
            cursor.execute(sql_check_details, (pedido_id,))
            detalles_count = cursor.fetchone()[0]
            
            if detalles_count > 0:
                print(f"No se puede eliminar el pedido {pedido_id} porque tiene detalles asociados.")
                return False  # Retornar False para indicar que no se eliminó

            sql_delete_details = "DELETE FROM detalles_pedido WHERE pedido_id = %s"
            cursor.execute(sql_delete_details, (pedido_id,))
            
            sql_delete_order = "DELETE FROM pedidos WHERE id = %s"
            cursor.execute(sql_delete_order, (pedido_id,))

        conexion.commit()
        print(f"Pedido {pedido_id} eliminado con éxito.")
        return True  # Retornar True para indicar que se eliminó exitosamente

    except pymysql.MySQLError as e:
        conexion.rollback()
        print(f"Error al eliminar el pedido: {str(e)}")
        raise e  # Re-lanzar la excepción para ser manejada más arriba

    finally:
        conexion.close()

def editar_pedido(pedido_id, direccion, ciudad, estado, pais, fecha_pedido, estado_pedido):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_direccion = """
                UPDATE direcciones 
                SET direccion = %s, ciudad = %s, estado = %s, pais = %s
                WHERE id = (SELECT direccion_id FROM pedidos WHERE id = %s)
            """
            cursor.execute(sql_direccion, (direccion, ciudad, estado, pais, pedido_id))
            
            sql_pedido = """
                UPDATE pedidos 
                SET fecha_pedido = %s, estado = %s
                WHERE id = %s
            """
            cursor.execute(sql_pedido, (fecha_pedido, estado_pedido, pedido_id))

        conexion.commit()
    except MySQLdb.Error as e:
        conexion.rollback()
        print(f"Error al editar el pedido: {str(e)}")
        raise e
    finally:
        conexion.close()


