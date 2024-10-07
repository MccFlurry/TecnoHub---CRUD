from bd import obtener_conexion
from clase.clase_usuario import Usuario
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# Inserta un nuevo usuario con la contraseña hash
def insertar_usuario(nombre, apellido, email, contrasena, tipo, foto):
    conexion = obtener_conexion()
    hashed_password = generate_password_hash(contrasena)  # Genera el hash de la contraseña
    with conexion.cursor() as cursor:
        sql = "INSERT INTO usuarios(nombre, apellido, email, contraseña, tipo, foto) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, apellido, email, hashed_password, tipo, foto))
    conexion.commit()
    conexion.close()

# Obtiene un usuario por su ID
def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor(DictCursor) as cursor:
        sql = """
        SELECT id, nombre, apellido, email, tipo, foto, fecha_registro, contraseña
        FROM usuarios
        WHERE id = %s
        """
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                id=row['id'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                tipo=row['tipo'],
                foto=row['foto'],
                fecha_registro=row['fecha_registro'],
                contraseña=row['contraseña']
            )
    conexion.close()
    return usuario

def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, apellido, email, contraseña, tipo, foto, fecha_registro FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(**row)
    conexion.close()
    return usuario

def actualizar_usuario(id, nombre, apellido, email, tipo, foto=None, nueva_contrasena=None):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        if nueva_contrasena:  # Si se proporciona una nueva contraseña, generamos un nuevo hash
            hashed_password = generate_password_hash(nueva_contrasena)
            sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s, contraseña = %s WHERE id = %s"
            cursor.execute(sql, (nombre, apellido, email, tipo, foto, hashed_password, id))
        else:  # Si no hay nueva contraseña, solo actualizamos los otros campos
            sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, tipo = %s, foto = %s WHERE id = %s"
            cursor.execute(sql, (nombre, apellido, email, tipo, foto, id))
    conexion.commit()
    conexion.close()

def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
    conexion.commit()
    conexion.close()

def contar_usuarios():
    conexion = obtener_conexion()
    total_usuarios = 0
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT COUNT(*) as total FROM usuarios"
        cursor.execute(sql)
        total_usuarios = cursor.fetchone()['total']
    conexion.close()
    return total_usuarios

def obtener_todos_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor(DictCursor) as cursor:
        # Incluye 'contraseña' en la consulta SQL
        sql = "SELECT id, nombre, apellido, email, tipo, foto, contraseña, fecha_registro FROM usuarios"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            usuario = Usuario(
                id=row['id'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                tipo=row['tipo'],
                foto=row['foto'],
                fecha_registro=row['fecha_registro'],
                contraseña=row['contraseña']
            )
            usuarios.append(usuario)
    conexion.close()
    return usuarios