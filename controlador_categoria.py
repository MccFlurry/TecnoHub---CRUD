from bd import obtener_conexion


def insertar_categoria(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="insert into categoria(nombre) values (%s)"
        cursor.execute(sql,(nombre))
    conexion.commit()
    conexion.close()

def obtener_categorias():
    conexion = obtener_conexion()
    categorias = []
    with conexion.cursor() as cursor:
        sql="Select id, nombre from categoria"
        cursor.execute(sql)
        categorias = cursor.fetchall()
    conexion.close()
    return categorias

def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("delete from categoria where id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_categoria_por_id(id):
    conexion = obtener_conexion()
    categoria = None
    with conexion.cursor() as cursor:
        sql="Select id, nombre from categoria where id = %s"        
        cursor.execute(sql,(id)) 
        categoria = cursor.fetchone()
    conexion.close()
    return categoria

def actualizar_categoria(nombre,id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql="update categoria set nombre = %s where id = %s "
        cursor.execute(sql,(nombre,id))
    conexion.commit()
    conexion.close()   
