from bd import obtener_conexion
from clase.clase_usuario import Usuario
from pymysql.cursors import DictCursor
import bcrypt
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def insertar_usuario(nombre, apellido, email, contrasena, tipo, foto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            hashed_password = hash_password(contrasena)
            sql = "INSERT INTO usuarios(nombre, apellido, email, contrasena, tipo, foto) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, apellido, email, hashed_password, tipo, foto))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False
    finally:
        conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, tipo, foto, fecha_registro, contrasena FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(**row)
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
    finally:
        conexion.close()
    return usuario

def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, contrasena, tipo, foto, fecha_registro FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(**row)
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
    finally:
        conexion.close()
    return usuario

def actualizar_usuario(id, nombre, apellido, email, tipo, foto=None, nueva_contrasena=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            if nueva_contrasena:
                hashed_password = hash_password(nueva_contrasena)
                sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s, contrasena = %s WHERE id = %s"
                cursor.execute(sql, (nombre, apellido, email, tipo, foto, hashed_password, id))
            else:
                sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s WHERE id = %s"
                cursor.execute(sql, (nombre, apellido, email, tipo, foto, id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False
    finally:
        conexion.close()

def eliminar_usuario(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        conexion.close()

def contar_usuarios():
    conexion = obtener_conexion()
    total_usuarios = 0
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT COUNT(*) as total FROM usuarios"
            cursor.execute(sql)
            total_usuarios = cursor.fetchone()['total']
    except Exception as e:
        print(f"Error al contar usuarios: {e}")
    finally:
        conexion.close()
    return total_usuarios

def obtener_todos_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    try:
        with conexion.cursor(DictCursor) as cursor:
            sql = "SELECT id, nombre, apellido, email, tipo, foto, contrasena, fecha_registro FROM usuarios"
            cursor.execute(sql)
            rows = cursor.fetchall()
            usuarios = [Usuario(**row) for row in rows]
    except Exception as e:
        print(f"Error al obtener todos los usuarios: {e}")
    finally:
        conexion.close()
    return usuarios

def tiene_pedidos_pendientes(usuario_id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            SELECT COUNT(*) 
            FROM pedidos 
            WHERE usuario_id = %s 
            AND estado IN ('pendiente', 'en_proceso', 'enviado')
            """
            cursor.execute(sql, (usuario_id,))
            cantidad = cursor.fetchone()[0]
            return cantidad > 0
    except Exception as e:
        logger.error(f"Error al verificar pedidos pendientes del usuario {usuario_id}: {str(e)}")
        raise
    finally:
        if conexion:
            conexion.close()

def iniciar_sesion(email, password):
    usuario = obtener_usuario_por_email(email)
    if usuario and check_password(usuario.contrasena, password):
        return {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'email': usuario.email,
            'tipo': usuario.tipo,
            'foto': usuario.foto
        }
    return None