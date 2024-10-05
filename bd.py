import pymysql 

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='',
                                db='py_paginaweb')