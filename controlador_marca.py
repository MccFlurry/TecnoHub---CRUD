from bd import obtener_conexion


def insertar_marca(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="insert into marca(nombre) values (%s)"
        cursor.execute(sql,(nombre))
    conexion.commit()
    conexion.close()

def obtener_marcas():
    conexion = obtener_conexion()
    marcas = []
    with conexion.cursor() as cursor:
        sql="Select id, nombre from marca"
        cursor.execute(sql)
        marcas = cursor.fetchall()
    conexion.close()
    return marcas

def eliminar_marca(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("delete from marca where id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_marca_por_id(id):
    conexion = obtener_conexion()
    marca = None
    with conexion.cursor() as cursor:
        sql="Select id, nombre from marca where id = %s"        
        cursor.execute(sql,(id)) 
        marca = cursor.fetchone()
    conexion.close()
    return marca

def actualizar_marca(nombre,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="update marca set nombre = %s where id = %s "
        cursor.execute(sql,(nombre,id))
    conexion.commit()
    conexion.close()   
