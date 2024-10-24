from bd import obtener_conexion
from clase.clase_direcciones import Direcciones
from pymysql.err import IntegrityError

def agregar_direccion(usuario_id, direccion, ciudad, estado, pais, codigo_postal):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print(f"Inserting address for usuario_id: {usuario_id}, address: {direccion}, ciudad: {ciudad}")

            validation_sql = "SELECT 1 FROM usuarios WHERE id = %s"
            cursor.execute(validation_sql, (usuario_id,))
            if not cursor.fetchone():
                raise ValueError(f"Usuario con ID {usuario_id} no existe.")

            sql = """
            INSERT INTO direcciones (usuario_id, direccion, ciudad, estado, pais, codigo_postal)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (usuario_id, direccion, ciudad, estado, pais, codigo_postal))
        
        conexion.commit()
        print("Dirección agregada con éxito.")
    except ValueError as e:
        print(f"Error de validación: {e}")
        conexion.rollback()
    except Exception as e:
        print(f"Error al agregar dirección: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_direcciones_usuario(usuario_id):
    conexion = obtener_conexion()
    direcciones = []
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, usuario_id, direccion, ciudad, estado, pais, codigo_postal 
            FROM direcciones 
            WHERE usuario_id = %s
            """
            cursor.execute(sql, (usuario_id,))
            for row in cursor.fetchall():
                direcciones.append({
                    'id': row[0],
                    'usuario_id': row[1],
                    'direccion': row[2],
                    'ciudad': row[3],
                    'estado': row[4],
                    'pais': row[5],
                    'codigo_postal': row[6]
                })
    except Exception as e:
        print(f"Error al obtener direcciones del usuario {usuario_id}: {e}")
    finally:
        conexion.close()
    return direcciones

def actualizar_direccion(id, direccion, ciudad, estado, pais, codigo_postal):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
            UPDATE direcciones 
            SET direccion = %s, ciudad = %s, estado = %s, pais = %s, codigo_postal = %s 
            WHERE id = %s
            """
            cursor.execute(sql, (direccion, ciudad, estado, pais, codigo_postal, id))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar la dirección con id {id}: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def eliminar_direccion(usuario_id, direccion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql_verificar = "SELECT id FROM direcciones WHERE id = %s AND usuario_id = %s"
            cursor.execute(sql_verificar, (direccion_id, usuario_id))
            direccion = cursor.fetchone()
            if not direccion:
                raise Exception("La dirección no existe o no te pertenece.")
            sql_eliminar = "DELETE FROM direcciones WHERE id = %s"
            cursor.execute(sql_eliminar, (direccion_id,))
        conexion.commit()
    except IntegrityError as e:
        print(f"IntegrityError en eliminar_direccion: {e}")
        conexion.rollback()
    except Exception as e:
        print(f"Excepción en eliminar_direccion: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_direccion_por_id(direccion_id):
    conexion = obtener_conexion()
    direccion = None
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT id, usuario_id, direccion, ciudad, estado, pais, codigo_postal 
            FROM direcciones 
            WHERE id = %s
            """
            cursor.execute(sql, (direccion_id,))
            row = cursor.fetchone()
            if row:
                direccion = Direcciones(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    except Exception as e:
        print(f"Error al obtener la dirección con id {direccion_id}: {e}")
    finally:
        conexion.close()
    return direccion