from bd import obtener_conexion
from clase.clase_pedido import Pedido
from clase.clase_detalle_pedido import DetallePedido
from datetime import datetime, timedelta

def crear_pedido(usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO pedidos(usuario_id, estado) VALUES (%s, 'pendiente')"
        cursor.execute(sql, (usuario_id,))
        pedido_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return pedido_id

def agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio_unitario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO detalles_pedido(pedido_id, producto_id, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (pedido_id, producto_id, cantidad, precio_unitario))
    conexion.commit()
    conexion.close()

def obtener_pedidos_por_usuario(usuario_id):
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, usuario_id, fecha_pedido, estado FROM pedidos WHERE usuario_id = %s ORDER BY fecha_pedido DESC"
        cursor.execute(sql, (usuario_id,))
        rows = cursor.fetchall()
        for row in rows:
            pedidos.append(Pedido(**row))
    conexion.close()
    return pedidos

def obtener_detalles_pedido(pedido_id):
    conexion = obtener_conexion()
    detalles = []
    with conexion.cursor() as cursor:
        sql = "SELECT id, pedido_id, producto_id, cantidad, precio_unitario FROM detalles_pedido WHERE pedido_id = %s"
        cursor.execute(sql, (pedido_id,))
        rows = cursor.fetchall()
        for row in rows:
            detalles.append(DetallePedido(**row))
    conexion.close()
    return detalles

def actualizar_estado_pedido(pedido_id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE pedidos SET estado = %s WHERE id = %s"
        cursor.execute(sql, (nuevo_estado, pedido_id))
    conexion.commit()
    conexion.close()

def obtener_todos_pedidos():
    conexion = obtener_conexion()
    pedidos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.usuario_id, p.fecha_pedido, p.estado, u.nombre, u.apellido, 
                   SUM(dp.cantidad * dp.precio_unitario) as total
            FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.id
            JOIN detalles_pedido dp ON p.id = dp.pedido_id
            GROUP BY p.id
            ORDER BY p.fecha_pedido DESC
        """)
        pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def obtener_pedido_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.usuario_id, p.fecha_pedido, p.estado, u.nombre, u.apellido
            FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.id = %s
        """, (id,))
        pedido = cursor.fetchone()
        
        if pedido:
            cursor.execute("""
                SELECT dp.id, dp.producto_id, dp.cantidad, dp.precio_unitario, pr.nombre
                FROM detalles_pedido dp
                JOIN productos pr ON dp.producto_id = pr.id
                WHERE dp.pedido_id = %s
            """, (id,))
            pedido['detalles'] = cursor.fetchall()
    
    conexion.close()
    return pedido

def actualizar_estado_pedido(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()

def contar_pedidos_pendientes():
    conexion = obtener_conexion()
    count = 0
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE estado = 'pendiente'")
        count = cursor.fetchone()[0]
    conexion.close()
    return count

def calcular_ingresos_mes():
    conexion = obtener_conexion()
    ingresos = 0
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
    conexion.close()
    return ingresos