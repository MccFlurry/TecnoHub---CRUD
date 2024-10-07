from bd import obtener_conexion
from clase.clase_usuario import Usuario
from pymysql.cursors import DictCursor

def insertar_usuario(nombre, apellido, email, contrasena, tipo, foto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql = "INSERT INTO usuarios(nombre, apellido, email, contraseña, tipo, foto) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, apellido, email, contrasena, tipo, foto))
    conexion.commit()
    conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor(DictCursor) as cursor:
        # Asegúrate de seleccionar 'contraseña' en la consulta SQL
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
        # Aquí mantenemos el nombre original 'contraseña' (con tilde)
        sql = "SELECT id, nombre, apellido, email, contraseña, tipo, foto, fecha_registro FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(**row)  # Pasa el diccionario completo con 'contraseña'
    conexion.close()
    return usuario

def actualizar_usuario(id, nombre, apellido, email, tipo, foto):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
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
        total_usuarios = cursor.fetchone()['total']  # Obtiene el número total de usuarios
    conexion.close()
    return total_usuarios

def obtener_todos_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, apellido, email, tipo, foto, contraseña, fecha_registro FROM usuarios"  # Incluye fecha_registro
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            usuario = Usuario(**row)
            usuarios.append(usuario)
    conexion.close()
    return usuarios
