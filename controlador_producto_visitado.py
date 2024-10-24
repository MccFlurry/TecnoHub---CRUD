from bd import obtener_conexion
from clase.clase_producto_visitado import ProductoVisitado

def registrar_visita(usuario_id, producto_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO productos_visitados (usuario_id, producto_id) VALUES (%s, %s)"
            cursor.execute(sql, (usuario_id, producto_id))
        conexion.commit()
    except Exception as e:
        print(f"Error al registrar la visita del producto {producto_id} para el usuario {usuario_id}: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_productos_visitados_recientes(usuario_id, limite=6):
    conexion = obtener_conexion()
    productos_visitados = []
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, usuario_id, producto_id, fecha_visita 
            FROM productos_visitados 
            WHERE usuario_id = %s 
            ORDER BY fecha_visita DESC 
            LIMIT %s
            """
            cursor.execute(sql, (usuario_id, limite))
            rows = cursor.fetchall()
            for row in rows:
                productos_visitados.append(ProductoVisitado(**row))
    except Exception as e:
        print(f"Error al obtener productos visitados recientes para el usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return productos_visitados