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
    with conexion.cursor(dictionary=True) as cursor:  # Configuramos para que devuelva un diccionario
        sql = "SELECT id, nombre, apellido, email, contraseña, tipo, foto FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(**row)
    conexion.close()
    return usuario

def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor(DictCursor) as cursor:
        sql = "SELECT id, nombre, apellido, email, contraseña, tipo, foto FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(**row)
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
