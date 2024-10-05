from bd import obtener_conexion

def insertar(nombre, apellidos, correo, contrasena, telefono_contacto, tipo_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO Usuario(nombre, apellidos, correo, contrasena, telefono_contacto, tipo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)""", (nombre, apellidos, correo, contrasena, telefono_contacto, tipo_usuario))
    conexion.commit()
    conexion.close()


def obtener():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idUsuario, nombre, apellidos, correo, telefono_contacto, tipo_usuario, fecha_registro FROM Usuario")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar(idUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Usuario WHERE idUsuario = %s", (idUsuario,))
    conexion.commit()
    conexion.close()


def obtener_por_id(idUsuario):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT idUsuario, nombre, apellidos, correo, telefono_contacto, tipo_usuario, fecha_registro FROM Usuario WHERE idUsuario = %s", (idUsuario,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario


def actualizar(nombre, apellidos, correo, contrasena, telefono_contacto, tipo_usuario, idUsuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""UPDATE Usuario
            SET nombre = %s, apellidos = %s, correo = %s, contrasena = %s, telefono_contacto = %s, tipo_usuario = %s
            WHERE idUsuario = %s""", (nombre, apellidos, correo, contrasena, telefono_contacto, tipo_usuario, idUsuario))
    conexion.commit()
    conexion.close()
