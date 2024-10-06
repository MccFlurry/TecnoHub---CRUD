import pymysql

def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        db="py_paginaweb",
    )
