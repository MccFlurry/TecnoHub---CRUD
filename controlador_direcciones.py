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
    except Exception as e:
        print(f"Error al agregar dirección: {e}")
    finally:
        conexion.close()


def obtener_direcciones_usuario(usuario_id):
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, usuario_id, direccion, ciudad, estado, pais, codigo_postal FROM direcciones WHERE usuario_id = %s", (usuario_id,))
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
    conexion.close()
    return direcciones

def actualizar_direccion(id, direccion, ciudad, estado, pais, codigo_postal):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "UPDATE direcciones SET direccion = %s, ciudad = %s, estado = %s, pais = %s, codigo_postal = %s WHERE id = %s"
        cursor.execute(sql, (direccion, ciudad, estado, pais, codigo_postal, id))
    conexion.commit()
    conexion.close()

def eliminar_direccion(usuario_id, direccion_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si la dirección pertenece al usuario
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
        raise e
    except Exception as e:
        print(f"Excepción en eliminar_direccion: {e}")
        raise e
    finally:
        conexion.close()

def obtener_direccion_por_id(direccion_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, usuario_id, direccion, ciudad, estado, pais, codigo_postal FROM direcciones WHERE id = %s", (direccion_id,))
        row = cursor.fetchone()
        if row:
            return Direcciones(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
    conexion.close()
    return None