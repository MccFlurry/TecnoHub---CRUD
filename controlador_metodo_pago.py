from clase.clase_metodo_pago import MetodoPago
from bd import obtener_conexion
from datetime import datetime
import bcrypt

def listar_metodos_pago(usuario_id):
    conexion = obtener_conexion()
    metodos_pago = []
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT id, usuario_id, tipo, numero_tarjeta, titular,
                        fecha_vencimiento, cvv, predeterminado, fecha_registro, activo
                        FROM metodos_pago WHERE usuario_id = %s AND activo = 1""",
                    (usuario_id,))
        resultados = cursor.fetchall()
        for resultado in resultados:
            # Enmascarar el número de tarjeta y CVV antes de enviar
            numero_tarjeta = '*' * 12 + resultado[3][-4:]
            metodo = MetodoPago(
                id=resultado[0],
                usuario_id=resultado[1],
                tipo=resultado[2],
                numero_tarjeta=numero_tarjeta,
                titular=resultado[4],
                fecha_vencimiento=resultado[5],
                cvv='***',
                predeterminado=resultado[7],
                fecha_registro=resultado[8],
                activo=resultado[9]
            )
            metodos_pago.append(metodo.to_dict())
    conexion.close()
    return metodos_pago

def obtener_metodo_pago(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""SELECT id, usuario_id, tipo, numero_tarjeta, titular,
                        fecha_vencimiento, cvv, predeterminado, fecha_registro, activo
                        FROM metodos_pago WHERE id = %s AND activo = 1""",
                    (id,))
        resultado = cursor.fetchone()
        if resultado:
            numero_tarjeta = '*' * 12 + resultado[3][-4:]
            metodo = MetodoPago(
                id=resultado[0],
                usuario_id=resultado[1],
                tipo=resultado[2],
                numero_tarjeta=numero_tarjeta,
                titular=resultado[4],
                fecha_vencimiento=resultado[5],
                cvv='***',
                predeterminado=resultado[7],
                fecha_registro=resultado[8],
                activo=resultado[9]
            )
            return metodo.to_dict()
    conexion.close()
    return None

def insertar_metodo_pago(metodo_pago):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Encriptar CVV antes de almacenar
            cvv_hash = bcrypt.hashpw(str(metodo_pago.cvv).encode('utf-8'), bcrypt.gensalt())
            
            # Si es predeterminado, actualizar otros métodos de pago
            if metodo_pago.predeterminado:
                cursor.execute("""UPDATE metodos_pago SET predeterminado = 0 
                                WHERE usuario_id = %s""", (metodo_pago.usuario_id,))
            
            # Formatear la fecha de vencimiento para agregar el día 01
            fecha_vencimiento = f"{metodo_pago.fecha_vencimiento}-01"
            
            # Insertar el nuevo método de pago
            cursor.execute("""INSERT INTO metodos_pago (usuario_id, tipo, numero_tarjeta,
                            titular, fecha_vencimiento, cvv, predeterminado, fecha_registro, activo)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), 1)""",
                        (metodo_pago.usuario_id, metodo_pago.tipo,
                         metodo_pago.numero_tarjeta, metodo_pago.titular,
                         fecha_vencimiento, cvv_hash,
                         metodo_pago.predeterminado))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar método de pago: {str(e)}")
        conexion.rollback()
        raise e
    finally:
        conexion.close()

def actualizar_metodo_pago(id, metodo_pago):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Si se marca como predeterminado, actualizar otros métodos de pago
            if metodo_pago.predeterminado:
                cursor.execute("""UPDATE metodos_pago SET predeterminado = 0 
                                WHERE usuario_id = %s AND id != %s""",
                            (metodo_pago.usuario_id, id))

            # Formatear la fecha de vencimiento para agregar el día 01
            fecha_vencimiento = f"{metodo_pago.fecha_vencimiento}-01"
            
            # Actualizar el método de pago
            cursor.execute("""UPDATE metodos_pago SET tipo = %s, titular = %s,
                            fecha_vencimiento = %s, predeterminado = %s
                            WHERE id = %s""",
                        (metodo_pago.tipo, metodo_pago.titular,
                         fecha_vencimiento, metodo_pago.predeterminado, id))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar método de pago: {str(e)}")
        conexion.rollback()
        raise e
    finally:
        conexion.close()

def eliminar_metodo_pago(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE metodos_pago SET activo = 0 WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def establecer_predeterminado(id, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Primero, quitar predeterminado de todos los métodos del usuario
        cursor.execute("""UPDATE metodos_pago SET predeterminado = 0 
                        WHERE usuario_id = %s""", (usuario_id,))
        # Establecer el nuevo método predeterminado
        cursor.execute("""UPDATE metodos_pago SET predeterminado = 1 
                        WHERE id = %s""", (id,))
    conexion.commit()
    conexion.close()