from bd import obtener_conexion


def insertar_modelo(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="insert into modelo(nombre) values (%s)"
        cursor.execute(sql,(nombre))
    conexion.commit()
    conexion.close()

def obtener_modelos():
    conexion = obtener_conexion()
    modelos = []
    with conexion.cursor() as cursor:
        sql="Select id, nombre from modelo"
        cursor.execute(sql)
        modelos = cursor.fetchall()
    conexion.close()
    return modelos

def eliminar_modelo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("delete from modelo where id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_modelo_por_id(id):
    conexion = obtener_conexion()
    modelo = None
    with conexion.cursor() as cursor:
        sql="Select id, nombre from modelo where id = %s"        
        cursor.execute(sql,(id)) 
        modelo = cursor.fetchone()
    conexion.close()
    return modelo

def actualizar_modelo(nombre,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="update modelo set nombre = %s where id = %s "
        cursor.execute(sql,(nombre,id))
    conexion.commit()
    conexion.close()   
