from bd import obtener_conexion
from clase.clase_usuario import Usuario
from pymysql.cursors import DictCursor
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def insertar_usuario(nombre, apellido, email, contraseña, tipo, foto):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            hashed_password = hash_password(contraseña)
            sql = "INSERT INTO usuarios(nombre, apellido, email, contraseña, tipo, foto) VALUES (%s, %s, %s, %s, %s, %s)"
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
            sql = "SELECT id, nombre, apellido, email, tipo, foto, fecha_registro, contraseña FROM usuarios WHERE id = %s"
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
            sql = "SELECT id, nombre, apellido, email, contraseña, tipo, foto, fecha_registro FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(**row)
    except Exception as e:
        print(f"Error al obtener usuario por email: {e}")
    finally:
        conexion.close()
    return usuario

def actualizar_usuario(id, nombre, apellido, email, tipo, foto=None, nueva_contraseña=None):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            if nueva_contraseña:
                hashed_password = hash_password(nueva_contraseña)
                sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s, contraseña = %s WHERE id = %s"
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
            sql = "SELECT id, nombre, apellido, email, tipo, foto, contraseña, fecha_registro FROM usuarios"
            cursor.execute(sql)
            rows = cursor.fetchall()
            usuarios = [Usuario(**row) for row in rows]
    except Exception as e:
        print(f"Error al obtener todos los usuarios: {e}")
    finally:
        conexion.close()
    return usuarios