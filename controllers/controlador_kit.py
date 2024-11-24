from bd import obtener_conexion
from clase.clase_kit import Kit
from clase.clase_producto import Producto
from pymysql.cursors import DictCursor
from utils.logger import log_database_operation, log_error

def crear_kit(usuario_id, celular_id, smartwatch_id, accesorios_id):
    conexion = obtener_conexion()
    try:
        # Validar que los productos existen
        with conexion.cursor() as cursor:
            # Verificar celular
            cursor.execute("SELECT id FROM productos WHERE id = %s", (celular_id,))
            if not cursor.fetchone():
                log_error(f"Error al crear kit: Celular {celular_id} no existe")
                raise ValueError("El celular especificado no existe")
            
            # Verificar smartwatch
            cursor.execute("SELECT id FROM productos WHERE id = %s", (smartwatch_id,))
            if not cursor.fetchone():
                log_error(f"Error al crear kit: Smartwatch {smartwatch_id} no existe")
                raise ValueError("El smartwatch especificado no existe")
            
            # Verificar accesorios
            cursor.execute("SELECT id FROM productos WHERE id = %s", (accesorios_id,))
            if not cursor.fetchone():
                log_error(f"Error al crear kit: Accesorio {accesorios_id} no existe")
                raise ValueError("El accesorio especificado no existe")
            
            # Verificar usuario
            cursor.execute("SELECT id FROM usuarios WHERE id = %s", (usuario_id,))
            if not cursor.fetchone():
                log_error(f"Error al crear kit: Usuario {usuario_id} no existe")
                raise ValueError("El usuario especificado no existe")
            
            # Si todas las validaciones pasan, crear el kit
            sql = "INSERT INTO kits (usuario_id, celular_id, smartwatch_id, accesorios_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario_id, celular_id, smartwatch_id, accesorios_id))
            kit_id = cursor.lastrowid
        conexion.commit()
        log_database_operation("INSERT", "kits", "SUCCESS", f"Kit {kit_id} creado para usuario {usuario_id}")
        return True, "Kit creado exitosamente"
    except ValueError as ve:
        log_error("Error de validación al crear kit", ve)
        conexion.rollback()
        return False, str(ve)
    except Exception as e:
        log_error("Error al crear kit", e)
        conexion.rollback()
        return False, "Error interno al crear el kit"
    finally:
        conexion.close()

def obtener_kits_usuario(usuario_id):
    conexion = obtener_conexion()
    kits = []
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT k.id, k.usuario_id, k.celular_id, k.smartwatch_id, k.accesorios_id, k.fecha_creacion,
                   c.nombre as celular_nombre, c.precio as celular_precio,
                   s.nombre as smartwatch_nombre, s.precio as smartwatch_precio,
                   a.nombre as accesorios_nombre, a.precio as accesorios_precio
            FROM kits k
            JOIN productos c ON k.celular_id = c.id
            JOIN productos s ON k.smartwatch_id = s.id
            JOIN productos a ON k.accesorios_id = a.id
            WHERE k.usuario_id = %s
            ORDER BY k.fecha_creacion DESC
            """
            cursor.execute(sql, (usuario_id,))
            rows = cursor.fetchall()
            for row in rows:
                kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['smartwatch_id'], row['accesorios_id'], row['fecha_creacion'])
                kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
                kit.smartwatch = Producto(row['smartwatch_id'], row['smartwatch_nombre'], '', row['smartwatch_precio'], 0, 0, '')
                kit.accesorios = Producto(row['accesorios_id'], row['accesorios_nombre'], '', row['accesorios_precio'], 0, 0, '')
                kits.append(kit)
            log_database_operation("SELECT", "kits", "SUCCESS", f"Obtenidos {len(kits)} kits para usuario {usuario_id}")
    except Exception as e:
        log_error(f"Error al obtener kits del usuario {usuario_id}", e)
    finally:
        conexion.close()
    return kits

def eliminar_kit(kit_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar que el kit existe
            cursor.execute("SELECT id FROM kits WHERE id = %s", (kit_id,))
            if not cursor.fetchone():
                log_error(f"Error al eliminar kit: Kit {kit_id} no existe")
                raise ValueError("El kit especificado no existe")
                
            sql = "DELETE FROM kits WHERE id = %s"
            cursor.execute(sql, (kit_id,))
        conexion.commit()
        log_database_operation("DELETE", "kits", "SUCCESS", f"Kit {kit_id} eliminado")
        return True, "Kit eliminado exitosamente"
    except ValueError as ve:
        log_error("Error de validación al eliminar kit", ve)
        conexion.rollback()
        return False, str(ve)
    except Exception as e:
        log_error(f"Error al eliminar el kit con id {kit_id}", e)
        conexion.rollback()
        return False, "Error interno al eliminar el kit"
    finally:
        conexion.close()

def obtener_kit_por_id(kit_id):
    conexion = obtener_conexion()
    kit = None
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = """
            SELECT k.id, k.usuario_id, k.celular_id, k.smartwatch_id, k.accesorios_id, k.fecha_creacion,
                   c.nombre as celular_nombre, c.precio as celular_precio,
                   s.nombre as smartwatch_nombre, s.precio as smartwatch_precio,
                   a.nombre as accesorios_nombre, a.precio as accesorios_precio
            FROM kits k
            JOIN productos c ON k.celular_id = c.id
            JOIN productos s ON k.smartwatch_id = s.id
            JOIN productos a ON k.accesorios_id = a.id
            WHERE k.id = %s
            """
            cursor.execute(sql, (kit_id,))
            row = cursor.fetchone()
            if row:
                kit = Kit(row['id'], row['usuario_id'], row['celular_id'], row['smartwatch_id'], row['accesorios_id'], row['fecha_creacion'])
                kit.celular = Producto(row['celular_id'], row['celular_nombre'], '', row['celular_precio'], 0, 0, '')
                kit.smartwatch = Producto(row['smartwatch_id'], row['smartwatch_nombre'], '', row['smartwatch_precio'], 0, 0, '')
                kit.accesorios = Producto(row['accesorios_id'], row['accesorios_nombre'], '', row['accesorios_precio'], 0, 0, '')
                log_database_operation("SELECT", "kits", "SUCCESS", f"Kit {kit_id} obtenido")
            else:
                log_error(f"Kit {kit_id} no encontrado")
    except Exception as e:
        log_error(f"Error al obtener el kit con id {kit_id}", e)
        raise e
    finally:
        conexion.close()
    return kit

def actualizar_kit(kit_id, celular_id, smartwatch_id, accesorios_id):
    conexion = obtener_conexion()
    try:
        # Validar que el kit existe
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM kits WHERE id = %s", (kit_id,))
            if not cursor.fetchone():
                log_error(f"Error al actualizar kit: Kit {kit_id} no existe")
                raise ValueError("El kit especificado no existe")
            
            # Verificar celular
            cursor.execute("SELECT id FROM productos WHERE id = %s", (celular_id,))
            if not cursor.fetchone():
                log_error(f"Error al actualizar kit: Celular {celular_id} no existe")
                raise ValueError("El celular especificado no existe")
            
            # Verificar smartwatch
            cursor.execute("SELECT id FROM productos WHERE id = %s", (smartwatch_id,))
            if not cursor.fetchone():
                log_error(f"Error al actualizar kit: Smartwatch {smartwatch_id} no existe")
                raise ValueError("El smartwatch especificado no existe")
            
            # Verificar accesorios
            cursor.execute("SELECT id FROM productos WHERE id = %s", (accesorios_id,))
            if not cursor.fetchone():
                log_error(f"Error al actualizar kit: Accesorio {accesorios_id} no existe")
                raise ValueError("El accesorio especificado no existe")
            
            # Si todas las validaciones pasan, actualizar el kit
            sql = """
                UPDATE kits 
                SET celular_id = %s, smartwatch_id = %s, accesorios_id = %s 
                WHERE id = %s
            """
            cursor.execute(sql, (celular_id, smartwatch_id, accesorios_id, kit_id))
        conexion.commit()
        log_database_operation("UPDATE", "kits", "SUCCESS", f"Kit {kit_id} actualizado")
        return True, "Kit actualizado exitosamente"
    except ValueError as ve:
        log_error("Error de validación al actualizar kit", ve)
        conexion.rollback()
        return False, str(ve)
    except Exception as e:
        log_error("Error al actualizar kit", e)
        conexion.rollback()
        return False, "Error interno al actualizar el kit"
    finally:
        conexion.close()