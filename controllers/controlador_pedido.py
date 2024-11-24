from bd import obtener_conexion
from clase.clase_pedido import Pedido
from clase.clase_detalle_pedido import DetallePedido
from datetime import datetime, timedelta
import pymysql as MySQLdb
import pymysql
from pymysql.cursors import DictCursor
import os
import csv

def crear_pedido(usuario_id, direccion_id, metodo_pago_id=None):
    conexion = obtener_conexion()
    fecha_pedido = datetime.now()
    try:
        with conexion.cursor() as cursor:
            if metodo_pago_id:
                sql = """INSERT INTO pedidos (usuario_id, direccion_id, metodo_pago_id, fecha_pedido, estado) 
                        VALUES (%s, %s, %s, %s, 'pendiente')"""
                cursor.execute(sql, (usuario_id, direccion_id, metodo_pago_id, fecha_pedido))
            else:
                sql = """INSERT INTO pedidos (usuario_id, direccion_id, fecha_pedido, estado) 
                        VALUES (%s, %s, %s, 'pendiente')"""
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
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT p.id, p.usuario_id, u.email, u.nombre, u.apellido, p.fecha_pedido, p.estado, 
                   d.direccion, d.ciudad, d.estado AS direccion_estado, d.pais, d.codigo_postal,
                   mp.tipo AS metodo_pago_tipo, mp.numero_tarjeta,
                   SUM(dp.precio_unitario * dp.cantidad) AS total
            FROM pedidos p
            JOIN direcciones d ON p.direccion_id = d.id
            JOIN detalles_pedido dp ON dp.pedido_id = p.id
            JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN metodos_pago mp ON p.metodo_pago_id = mp.id
            WHERE p.usuario_id = %s
            GROUP BY p.id, p.usuario_id, p.fecha_pedido, p.estado, d.direccion, d.ciudad, d.estado, 
                     d.pais, d.codigo_postal, u.email, u.nombre, u.apellido, mp.tipo, mp.numero_tarjeta
            """
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            for row in rows:
                row['direccion'] = {
                    'direccion': row['direccion'],
                    'ciudad': row['ciudad'],
                    'estado': row['direccion_estado'],
                    'pais': row['pais'],
                    'codigo_postal': row['codigo_postal']
                }
                if row['metodo_pago_tipo']:
                    row['metodo_pago'] = {
                        'tipo': row['metodo_pago_tipo'],
                        'numero_tarjeta': row['numero_tarjeta'][-4:] if row['numero_tarjeta'] else None
                    }
                pedidos.append(row)
    except MySQLdb.Error as e:
        print(f"Error al obtener los pedidos del usuario {usuario_id}: {str(e)}")
    finally:
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
    except MySQLdb.Error as e:
        print(f"Error al obtener los detalles del pedido {pedido_id}: {str(e)}")
    finally:
        conexion.close()
    return detalles

def actualizar_estado_pedido(pedido_id, nuevo_estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE pedidos SET estado = %s WHERE id = %s"
            cursor.execute(sql, (nuevo_estado, pedido_id))
            filas_afectadas = cursor.rowcount
        conexion.commit()
        return filas_afectadas > 0
    except MySQLdb.Error as e:
        conexion.rollback()
        print(f"Error al actualizar el estado del pedido: {str(e)}")
        raise e
    finally:
        conexion.close()

def obtener_todos_pedidos():
    conexion = obtener_conexion()
    pedidos = []
    try:
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
    except MySQLdb.Error as e:
        print(f"Error al obtener todos los pedidos: {str(e)}")
    finally:
        conexion.close()
    return pedidos

def obtener_pedido_por_id(id):
    conexion = obtener_conexion()
    pedido = None
    total = 0
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute("""
                SELECT p.id, p.usuario_id, p.fecha_pedido, p.estado, 
                       u.nombre, u.apellido, u.email, 
                       d.direccion, d.ciudad, d.estado AS direccion_estado, d.pais, d.codigo_postal,
                       mp.tipo AS metodo_pago_tipo, mp.numero_tarjeta
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                JOIN direcciones d ON p.direccion_id = d.id
                LEFT JOIN metodos_pago mp ON p.metodo_pago_id = mp.id
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
                
                # Formatear la información del método de pago
                if pedido['metodo_pago_tipo']:
                    pedido['metodo_pago'] = {
                        'tipo': pedido['metodo_pago_tipo'],
                        'numero_tarjeta': pedido['numero_tarjeta'][-4:] if pedido['numero_tarjeta'] else None
                    }
    except MySQLdb.Error as e:
        print(f"Error al obtener el pedido con id {id}: {str(e)}")
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
    except MySQLdb.Error as e:
        print(f"Error al contar los pedidos pendientes: {str(e)}")
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
    except MySQLdb.Error as e:
        print(f"Error al calcular los ingresos del mes: {str(e)}")
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
                return False

            sql_delete_details = "DELETE FROM detalles_pedido WHERE pedido_id = %s"
            cursor.execute(sql_delete_details, (pedido_id,))

            sql_delete_order = "DELETE FROM pedidos WHERE id = %s"
            cursor.execute(sql_delete_order, (pedido_id,))

        conexion.commit()
        print(f"Pedido {pedido_id} eliminado con éxito.")
        return True

    except pymysql.MySQLError as e:
        conexion.rollback()
        print(f"Error al eliminar el pedido: {str(e)}")
        raise e

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

def generar_reporte_ventas_diarias(fecha_inicio=None, fecha_fin=None):
    """
    Genera un reporte de ventas diarias
    
    Args:
        fecha_inicio (str, optional): Fecha de inicio del reporte en formato 'YYYY-MM-DD'
        fecha_fin (str, optional): Fecha de fin del reporte en formato 'YYYY-MM-DD'
    
    Returns:
        dict: Reporte de ventas diarias
    """
    conexion = obtener_conexion()
    reporte = []
    try:
        with conexion.cursor(DictCursor) as cursor:
            # Si no se proporcionan fechas, usar el último mes por defecto
            if not fecha_inicio or not fecha_fin:
                fecha_fin = datetime.now().strftime('%Y-%m-%d')
                fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            sql = """
            SELECT 
                DATE(fecha_pedido) AS fecha, 
                COUNT(DISTINCT id) AS num_pedidos, 
                SUM(total) AS total_ventas
            FROM (
                SELECT 
                    p.id, 
                    p.fecha_pedido, 
                    SUM(dp.cantidad * dp.precio_unitario) AS total
                FROM pedidos p
                JOIN detalles_pedido dp ON p.id = dp.pedido_id
                WHERE p.fecha_pedido BETWEEN %s AND %s
                GROUP BY p.id, p.fecha_pedido
            ) AS ventas_diarias
            GROUP BY fecha
            ORDER BY fecha
            """
            cursor.execute(sql, (fecha_inicio, fecha_fin))
            reporte = cursor.fetchall()
    except MySQLdb.Error as e:
        print(f"Error al generar reporte de ventas diarias: {str(e)}")
    finally:
        conexion.close()
    
    return reporte

def obtener_pedidos_por_estado(estado):
    """
    Obtiene los pedidos filtrados por estado
    
    Args:
        estado (str): Estado del pedido (pendiente, completado, cancelado, etc.)
    
    Returns:
        list: Lista de pedidos con el estado especificado
    """
    conexion = obtener_conexion()
    pedidos = []
    
    print(f"Buscando pedidos con estado: {estado}")
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT 
                p.id, 
                p.fecha_pedido, 
                p.estado, 
                COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) AS total
            FROM pedidos p
            LEFT JOIN detalles_pedido dp ON p.id = dp.pedido_id
            WHERE p.estado = %s
            GROUP BY p.id, p.fecha_pedido, p.estado
            ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(sql, (estado,))
            pedidos = cursor.fetchall()
            print(f"Pedidos encontrados: {len(pedidos)}")
            
            # Formatear los resultados
            pedidos = [{
                'id': p['id'],
                'fecha': p['fecha_pedido'].strftime('%Y-%m-%d %H:%M:%S'),
                'total': float(p['total']),
                'estado': p['estado']
            } for p in pedidos]
            
    except Exception as e:
        print(f"Error al obtener pedidos por estado {estado}: {str(e)}")
        raise Exception(f"Error al obtener pedidos por estado: {str(e)}")
    finally:
        conexion.close()
    
    return pedidos

def generar_reporte_ingresos_mensuales(anio=None):
    """
    Genera un reporte de ingresos mensuales
    
    Args:
        anio (int, optional): Año para el reporte. Si no se proporciona, se usa el año actual
    
    Returns:
        list: Reporte de ingresos mensuales
    """
    conexion = obtener_conexion()
    reporte = []
    
    # Si no se proporciona año, usar el año actual
    if anio is None:
        anio = datetime.now().year
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT 
                MONTH(fecha_pedido) AS mes, 
                COUNT(DISTINCT id) AS num_pedidos, 
                SUM(total) AS total_ingresos
            FROM (
                SELECT 
                    p.id, 
                    p.fecha_pedido, 
                    SUM(dp.cantidad * dp.precio_unitario) AS total
                FROM pedidos p
                JOIN detalles_pedido dp ON p.id = dp.pedido_id
                WHERE YEAR(p.fecha_pedido) = %s
                GROUP BY p.id, p.fecha_pedido
            ) AS ingresos_mensuales
            GROUP BY mes
            ORDER BY mes
            """
            cursor.execute(sql, (anio,))
            reporte = cursor.fetchall()
    except MySQLdb.Error as e:
        print(f"Error al generar reporte de ingresos mensuales: {str(e)}")
    finally:
        conexion.close()
    
    return reporte

def exportar_pedidos(formato='csv', fecha_inicio=None, fecha_fin=None):
    """
    Exporta pedidos en un formato específico
    
    Args:
        formato (str, optional): Formato de exportación (csv, json, etc.)
        fecha_inicio (str, optional): Fecha de inicio del reporte
        fecha_fin (str, optional): Fecha de fin del reporte
    
    Returns:
        dict: Diccionario con datos de pedidos y ruta del archivo si es CSV
    """
    conexion = obtener_conexion()
    datos = []
    
    print(f"Exportando pedidos - formato: {formato}, fecha_inicio: {fecha_inicio}, fecha_fin: {fecha_fin}")
    
    # Si no se proporcionan fechas, usar el último mes por defecto
    if not fecha_inicio or not fecha_fin:
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"Fechas ajustadas - inicio: {fecha_inicio}, fin: {fecha_fin}")
    
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT 
                p.id, 
                p.usuario_id, 
                CONCAT(u.nombre, ' ', u.apellido) as cliente,
                p.fecha_pedido, 
                p.estado,
                d.direccion,
                d.ciudad,
                d.pais,
                mp.tipo as metodo_pago,
                SUM(dp.cantidad * dp.precio_unitario) AS total
            FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.id
            JOIN direcciones d ON p.direccion_id = d.id
            LEFT JOIN metodos_pago mp ON p.metodo_pago_id = mp.id
            JOIN detalles_pedido dp ON p.id = dp.pedido_id
            WHERE p.fecha_pedido BETWEEN %s AND %s
            GROUP BY p.id, p.usuario_id, u.nombre, u.apellido, p.fecha_pedido, p.estado, d.direccion, d.ciudad, d.pais, mp.tipo
            ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(sql, (fecha_inicio, fecha_fin))
            datos = cursor.fetchall()
            print(f"Datos obtenidos: {len(datos)} pedidos")
            
            if formato.lower() == 'csv':
                # Asegurar que existe el directorio de exportaciones
                if not os.path.exists('exports'):
                    print("Creando directorio exports")
                    os.makedirs('exports')
                
                # Generar nombre de archivo único con timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                nombre_archivo = f'pedidos_{timestamp}.csv'
                ruta_archivo = os.path.join('exports', nombre_archivo)
                print(f"Ruta del archivo: {ruta_archivo}")
                
                # Escribir datos al archivo CSV
                with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
                    writer = csv.DictWriter(archivo_csv, fieldnames=[
                        'id', 'usuario_id', 'cliente', 'fecha_pedido', 'estado',
                        'direccion', 'ciudad', 'pais', 'metodo_pago', 'total'
                    ])
                    writer.writeheader()
                    for pedido in datos:
                        # Formatear la fecha para el CSV
                        pedido['fecha_pedido'] = pedido['fecha_pedido'].strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow(pedido)
                print(f"Archivo CSV generado exitosamente")
                
                return {
                    'datos': datos,
                    'archivo': nombre_archivo,
                    'ruta': ruta_archivo
                }
    except MySQLdb.Error as e:
        print(f"Error al exportar pedidos: {str(e)}")
        raise Exception(f"Error al exportar pedidos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise e
    finally:
        conexion.close()
    
    return {'datos': datos}