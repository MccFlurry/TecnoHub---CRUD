import pymysql

def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        db="py_paginaweb",
    )

    # def obtener_conexion():
    # return pymysql.connect(
    #     host="Grupo5DAW.mysql.pythonanywhere-services.com",
    #     user="Grupo5DAW",
    #     passwd="mrmilk12",
    #     db="Grupo5DAW$py_paginaweb",
    # )
