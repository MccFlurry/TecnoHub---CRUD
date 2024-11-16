from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response, Blueprint, current_app
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from flask_wtf.csrf import generate_csrf
import os
import re
import logging
from bd import obtener_conexion
from pymysql.err import IntegrityError
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import controlador_usuario
import controlador_categorias
import controlador_producto
import controlador_pedido
import controlador_kit
import controlador_favorito
import controlador_direcciones
import controlador_opinion
import controlador_notificaciones
import controlador_ubicacion
import controlador_metodo_pago
from clase.clase_metodo_pago import MetodoPago

# PROYECTO ACTUALIZADO 17/11/2024 NO OLVIDAR IMPLEMENTAR PAPIS

app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key = 'tu_clave_secreta'
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
logger = logging.getLogger(__name__)

# Agregar la configuración de CSRF para evitar el KeyError
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
app.config['WTF_CSRF_FIELD_NAME'] = 'csrf_token'
app.config['WTF_CSRF_HEADERS'] = ['X-CSRF-Token', 'X-CSRFToken', 'X-XSRF-Token']
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Decorador login_required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Decorador admin_required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session or session.get('usuario_tipo') != 'administrador':
            flash('No tienes permiso para acceder a esta página', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Crear el Blueprint de administración
admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates/admin', static_folder='static')


# Aplicar la protección CSRF al Blueprint de administración
@admin_bp.before_request
def admin_csrf_protect():
    if request.method == "POST":
        if 'WTF_CSRF_METHODS' in current_app.config:
            csrf.protect()
        else:
            print("Advertencia: WTF_CSRF_METHODS no está configurado.")


@admin_bp.app_context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

# Rutas fuera del Blueprint (no tendrán protección CSRF)
@app.route('/')
def home():
    productos_destacados = controlador_producto.obtener_productos_destacados()
    categorias = controlador_categorias.obtener_todas_categorias()

    productos_visitados = request.cookies.get('productos_visitados', '')
    productos_recientes = []

    if productos_visitados:
        productos_ids = [int(id) for id in productos_visitados.split(',') if id.isdigit()]
        if productos_ids:
            productos_recientes = controlador_producto.obtener_productos_por_ids(productos_ids)

    return render_template('home.html', 
                           productos=productos_destacados, 
                           categorias=categorias, 
                           productos_recientes=productos_recientes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        contrasena = request.form['contrasena']
        
        # Validación básica del formato del email en el backend
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            flash('Por favor, ingresa un correo electrónico válido', 'error')
            return render_template('login.html')
        
        usuario = controlador_usuario.obtener_usuario_por_email(email)
        
        if usuario and controlador_usuario.check_password(usuario.contrasena, contrasena):
            session['usuario_id'] = usuario.id
            session['usuario_tipo'] = usuario.tipo
            session['usuario_nombre'] = usuario.nombre.split()[0] if usuario.nombre else ""
            session['usuario_apellido'] = usuario.apellido.split()[0] if usuario.apellido else ""
            flash('¡Bienvenido! Has iniciado sesión exitosamente', 'success')
            
            if usuario.tipo == 'administrador':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Credenciales inválidas. Por favor, verifica tu correo y contrasena', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contrasena = request.form['contrasena']
        
        if controlador_usuario.insertar_usuario(nombre, apellido, email, contrasena, 'cliente', None):
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro. Por favor, intenta de nuevo.', 'error')

    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/categorias/<int:id>')
def categorias(id):
    categoria = controlador_categorias.obtener_categorias_por_id(id)
    if not categoria:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('home'))
    productos = controlador_producto.obtener_productos_por_categorias(id)
    return render_template('categorias.html', categoria=categoria, productos=productos)

@app.route('/categorias')
def todas_categorias():
    categorias = controlador_categorias.obtener_todas_categorias()
    return render_template('categorias.html', categorias=categorias)

@app.context_processor
def inject_categories():
    categorias = controlador_categorias.obtener_todas_categorias()
    return dict(categorias=categorias)

@app.route('/arma-tu-kit', methods=['GET', 'POST'])
def arma_tu_kit():
    if request.method == 'POST':
        celular_id = request.form.get('celular_id')
        smartwatch_id = request.form.get('smartwatch_id')
        accesorios_id = request.form.get('accesorios_id')
        usuario_id = session.get('usuario_id')

        if usuario_id:
            carrito = session.get('carrito', [])
            
            if celular_id:
                celular = controlador_producto.obtener_producto_por_id(int(celular_id))
                if celular:
                    carrito.append({
                        'producto_id': celular.id,
                        'nombre': celular.nombre,
                        'precio': float(celular.precio),
                        'cantidad': 1
                    })
            
            if smartwatch_id:
                smartwatch = controlador_producto.obtener_producto_por_id(int(smartwatch_id))
                if smartwatch:
                    carrito.append({
                        'producto_id': smartwatch.id,
                        'nombre': smartwatch.nombre,
                        'precio': float(smartwatch.precio),
                        'cantidad': 1
                    })
            
            if accesorios_id:
                accesorio = controlador_producto.obtener_producto_por_id(int(accesorios_id))
                if accesorio:
                    carrito.append({
                        'producto_id': accesorio.id,
                        'nombre': accesorio.nombre,
                        'precio': float(accesorio.precio),
                        'cantidad': 1
                    })

            session['carrito'] = carrito
            flash('Kit agregado al carrito con éxito', 'success')
            return redirect(url_for('carrito'))
        else:
            flash('Debes iniciar sesión para crear un kit', 'error')
            return redirect(url_for('login'))

    celulares = controlador_producto.obtener_productos_por_categorias(1) 
    smartwatch = controlador_producto.obtener_productos_por_categorias(2)
    accesorios = controlador_producto.obtener_productos_por_categorias(3)

    return render_template('arma_tu_kit.html', celulares=celulares, smartwatch=smartwatch, accesorios=accesorios)

@app.route('/agregar-favorito/<int:producto_id>', methods=['POST'])
@login_required
def agregar_favorito(producto_id):
    usuario_id = session.get('usuario_id')
    try:
        if controlador_favorito.existe_favorito(usuario_id, producto_id):
            return jsonify(success=False, message="El producto ya está en tus favoritos")
        
        controlador_favorito.agregar_favorito(usuario_id, producto_id)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error al agregar favorito: {e}")
        return jsonify(success=False, message="Error interno, inténtalo nuevamente")

@app.route('/eliminar-favorito/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_favorito(producto_id):
    usuario_id = session.get('usuario_id')
    try:
        controlador_favorito.eliminar_favorito(usuario_id, producto_id)
        return redirect(url_for('mis_favoritos'))
    except Exception as e:
        print(f"Error en eliminar_favorito: {e}")
        return jsonify(success=False, message="Error interno, inténtalo nuevamente")

@app.route('/mis-favoritos')
@login_required
def mis_favoritos():
    usuario_id = session.get('usuario_id')
    favoritos = controlador_favorito.obtener_favoritos_usuario(usuario_id)
    productos_favoritos = [controlador_producto.obtener_producto_por_id(fav.producto_id) for fav in favoritos]
    return render_template('mis_favoritos.html', productos=productos_favoritos)

@app.route('/agregar-direccion', methods=['GET', 'POST'])
@login_required
def agregar_direccion():
    if request.method == 'POST':
        try:
            usuario_id = session.get('usuario_id')
            if not usuario_id:
                flash('Error: No se pudo identificar al usuario.', 'error')
                return redirect(url_for('agregar_direccion'))

            datos = {
                'usuario_id': usuario_id,
                'distrito_id': request.form.get('distrito_id'),
                'direccion': request.form.get('direccion'),
                'numero': request.form.get('numero'),
                'departamento': request.form.get('departamento'),
                'referencia': request.form.get('referencia'),
                'direccion_predeterminada': bool(request.form.get('direccion_predeterminada', False))
            }

            # Validar campos requeridos
            if not all([datos['distrito_id'], datos['direccion']]):
                flash('Por favor complete todos los campos requeridos.', 'error')
                return redirect(url_for('agregar_direccion'))

            controlador_direcciones.agregar_direccion(datos)
            flash('Dirección agregada con éxito', 'success')
            return redirect(url_for('mis_direcciones'))

        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('agregar_direccion'))
        except Exception as e:
            logger.error(f"Error al agregar dirección: {str(e)}")
            flash('Ocurrió un error al agregar la dirección.', 'error')
            return redirect(url_for('agregar_direccion'))

    # GET: Obtener datos para el formulario
    try:
        paises = controlador_ubicacion.obtener_todos_paises()
        return render_template('agregar_direccion.html', paises=paises)
    except Exception as e:
        logger.error(f"Error al cargar formulario de dirección: {str(e)}")
        flash('Error al cargar el formulario.', 'error')
        return redirect(url_for('mis_direcciones'))

@app.route('/editar-direccion/<int:direccion_id>', methods=['GET', 'POST'])
@login_required
def editar_direccion(direccion_id):
    try:
        direccion = controlador_direcciones.obtener_direccion_por_id(direccion_id)
        if not direccion:
            flash('Dirección no encontrada', 'error')
            return redirect(url_for('mis_direcciones'))

        if request.method == 'POST':
            # Recoger datos del formulario
            datos = {
                'direccion': request.form.get('direccion'),
                'ciudad': request.form.get('ciudad_id'),
                'estado': request.form.get('estado_id'),
                'pais': request.form.get('pais_id'),
                'codigo_postal': request.form.get('codigo_postal'),
                'direccion_predeterminada': bool(request.form.get('direccion_predeterminada', False))
            }

            # Validar campos requeridos
            campos_requeridos = ['direccion', 'ciudad', 'estado', 'pais', 'codigo_postal']
            if not all(datos.get(campo) for campo in campos_requeridos):
                flash('Por favor complete todos los campos requeridos.', 'error')
                return redirect(url_for('editar_direccion', direccion_id=direccion_id))

            controlador_direcciones.actualizar_direccion(direccion_id, datos)
            flash('Dirección actualizada con éxito', 'success')
            return redirect(url_for('mis_direcciones'))

        # GET: Obtener datos para los combo boxes
        paises = controlador_ubicacion.obtener_todos_paises()
        estados = controlador_ubicacion.obtener_estados_por_pais(direccion['pais']) if direccion['pais'] else []
        ciudades = controlador_ubicacion.obtener_ciudades_por_estado(direccion['estado']) if direccion['estado'] else []
        
        return render_template('editar_direccion.html', 
                             direccion=direccion,
                             paises=paises,
                             estados=estados,
                             ciudades=ciudades)

    except Exception as e:
        logger.error(f"Error en editar_direccion: {str(e)}")
        flash('Ocurrió un error al procesar la solicitud.', 'error')
        return redirect(url_for('mis_direcciones'))
    
@app.route('/establecer-direccion-predeterminada/<int:direccion_id>', methods=['POST'])
@login_required
def establecer_direccion_predeterminada(direccion_id):
    try:
        usuario_id = session.get('usuario_id')
        resultado = controlador_direcciones.establecer_direccion_predeterminada(
            usuario_id, direccion_id
        )
        if resultado:
            flash('Dirección establecida como predeterminada', 'success')
        else:
            flash('No se pudo establecer la dirección como predeterminada', 'error')
    except Exception as e:
        logger.error(f"Error al establecer dirección predeterminada: {str(e)}")
        flash('Error al procesar la solicitud', 'error')
    
    return redirect(url_for('mis_direcciones'))
    
@app.route('/eliminar-direccion/<int:direccion_id>', methods=['POST'])
@login_required
def eliminar_direccion(direccion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Debes iniciar sesión para realizar esta acción.', 'error')
        return redirect(url_for('login'))
        
    try:
        resultado = controlador_direcciones.eliminar_direccion(usuario_id, direccion_id)
        if resultado:
            flash('Dirección eliminada con éxito.', 'success')
        else:
            flash('No se puede eliminar la dirección porque está asociada a pedidos existentes.', 'error')
            
    except IntegrityError as e:
        logger.error(f"Error de integridad al eliminar dirección {direccion_id}: {str(e)}")
        if e.args[0] == 1451:
            flash('No se puede eliminar la dirección porque está asociada a pedidos existentes.', 'error')
        else:
            flash('Error de integridad en la base de datos.', 'error')
            
    except ValueError as e:
        logger.error(f"Error de validación al eliminar dirección {direccion_id}: {str(e)}")
        if str(e) == "La dirección no existe o no te pertenece.":
            flash('La dirección no existe o no te pertenece.', 'error')
        else:
            flash('Error de validación al procesar la solicitud.', 'error')
            
    except Exception as e:
        logger.error(f"Error inesperado al eliminar dirección {direccion_id}: {str(e)}")
        flash('Ocurrió un error inesperado. Por favor, inténtalo nuevamente.', 'error')

    return redirect(url_for('mis_direcciones'))

@app.route('/mis-direcciones')
@login_required
def mis_direcciones():
    direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
    return render_template('mis_direcciones.html', direcciones=direcciones)

@app.route('/producto/<int:id>')
def producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    opiniones = controlador_opinion.obtener_opiniones_producto(id)
    productos_relacionados = controlador_producto.obtener_productos_relacionados(id)
    promedio_calificacion = controlador_opinion.calcular_calificacion_promedio(id)

    productos_visitados = request.cookies.get('productos_visitados', '')

    productos_visitados = productos_visitados.split(',') if productos_visitados else []

    if str(id) not in productos_visitados:
        productos_visitados.append(str(id))

    if len(productos_visitados) > 6:
        productos_visitados = productos_visitados[-6:]

    response = make_response(render_template(
        'producto.html', 
        producto=producto, 
        opiniones=opiniones, 
        productos_relacionados=productos_relacionados,
        promedio_calificacion=promedio_calificacion 
    ))

    response.set_cookie('productos_visitados', ','.join(productos_visitados), max_age=30*24*60*60)  # 30 días

    return response

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria', '').strip()

    if not query:
        flash('Debe ingresar un término de búsqueda', 'error')
        return redirect(url_for('home'))

    categorias = controlador_categorias.obtener_todas_categorias()
    productos = controlador_producto.buscar_productos(query)

    return render_template('resultados_busqueda.html', productos=productos, query=query, categorias=categorias)

@app.route('/mis-kits')
@login_required
def mis_kits():
    usuario_id = session['usuario_id']
    kits = controlador_kit.obtener_kits_usuario(usuario_id)
    return render_template('mis_kits.html', kits=kits)

@app.route('/eliminar-kit/<int:kit_id>', methods=['POST'])
@login_required
def eliminar_kit(kit_id):
    kit = controlador_kit.obtener_kit_por_id(kit_id)
    if kit and kit.usuario_id == session['usuario_id']:
        controlador_kit.eliminar_kit(kit_id)
        flash('Kit eliminado con éxito', 'success')
    else:
        flash('No tienes permiso para eliminar este kit', 'error')
    return redirect(url_for('mis_kits'))

@app.route('/agregar-al-carrito/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    producto = controlador_producto.obtener_producto_por_id(producto_id)

    if not producto:
        flash('El producto no existe', 'error')
        return redirect(url_for('home'))

    if 'carrito' not in session:
        session['carrito'] = []

    for item in session['carrito']:
        if item['producto_id'] == producto_id:
            item['cantidad'] += cantidad
            session.modified = True
            flash('Producto actualizado en el carrito', 'success')
            return redirect(url_for('carrito'))

    session['carrito'].append({
        'producto_id': producto_id,
        'cantidad': cantidad,
        'nombre': producto.nombre,
        'precio': float(producto.precio)
    })
    session.modified = True
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('carrito'))

@app.route('/carrito')
@login_required
def carrito():
    total = sum(int(item['cantidad']) * float(item['precio']) for item in session.get('carrito', []))
    return render_template('carrito.html', carrito=session.get('carrito', []), total=total)

@app.route('/actualizar-carrito', methods=['POST'])
@login_required
def actualizar_carrito():
    try:
        # Cambiar de request.get_json() a request.form
        producto_id = int(request.form.get('producto_id'))
        nueva_cantidad = int(request.form.get('cantidad'))
        
        if 'carrito' in session:
            carrito_actualizado = []
            total = 0
            for item in session['carrito']:
                if item['producto_id'] == producto_id:
                    if nueva_cantidad > 0:
                        item['cantidad'] = nueva_cantidad
                        carrito_actualizado.append(item)
                else:
                    carrito_actualizado.append(item)
                total += item['precio'] * item['cantidad']
            
            session['carrito'] = carrito_actualizado
            session.modified = True
            flash('Carrito actualizado exitosamente', 'success')
            
        return redirect(url_for('carrito'))
            
    except Exception as e:
        app.logger.error(f'Error al actualizar carrito: {str(e)}')
        flash('Error al actualizar el carrito', 'error')
        return redirect(url_for('carrito'))

@app.route('/eliminar-del-carrito/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(producto_id):
    try:
        if 'carrito' in session:
            producto_nombre = next((item['nombre'] for item in session['carrito'] 
                                  if item['producto_id'] == producto_id), 'Producto')
            
            carrito_actualizado = [item for item in session['carrito'] 
                                 if item['producto_id'] != producto_id]
            
            session['carrito'] = carrito_actualizado
            session.modified = True
            
            flash(f'{producto_nombre} eliminado del carrito', 'success')
            
        return redirect(url_for('carrito'))
            
    except Exception as e:
        app.logger.error(f'Error al eliminar del carrito: {str(e)}')
        flash('Error al eliminar el producto del carrito', 'error')
        return redirect(url_for('carrito'))

@app.route('/realizar-pedido', methods=['GET', 'POST'])
@login_required
def realizar_pedido():
    try:
        if request.method == 'POST':
            # Verificar si el carrito está vacío
            if 'carrito' not in session or not session['carrito']:
                flash('Tu carrito está vacío', 'error')
                return redirect(url_for('carrito'))

            # Obtener la dirección de envío seleccionada
            direccion_id = request.form.get('direccion_id')
            if not direccion_id:
                flash('Debes seleccionar una dirección de envío', 'error')
                return redirect(url_for('realizar_pedido'))

            # Obtener el método de pago seleccionado (opcional)
            metodo_pago_id = request.form.get('metodo_pago_id')

            # Crear el pedido
            usuario_id = session.get('usuario_id')
            if not usuario_id:
                flash('No se pudo identificar al usuario. Por favor, inicia sesión nuevamente.', 'error')
                return redirect(url_for('login'))

            pedido_id = controlador_pedido.crear_pedido(
                usuario_id=usuario_id,
                direccion_id=int(direccion_id),
                metodo_pago_id=int(metodo_pago_id) if metodo_pago_id else None
            )
            total = 0

            # Agregar los detalles del pedido
            for item in session['carrito']:
                try:
                    producto_id = item.get('producto_id')
                    cantidad = int(item.get('cantidad'))
                    precio = float(item.get('precio'))

                    controlador_pedido.agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio)
                    total += cantidad * precio

                    # Actualizar el stock del producto
                    controlador_producto.actualizar_stock(producto_id, -cantidad)
                except Exception as detalle_error:
                    app.logger.error(f'Error al agregar detalle del pedido: {str(detalle_error)}')
                    flash('Ocurrió un error al agregar un producto al pedido.', 'error')
                    return redirect(url_for('realizar_pedido'))

            # Limpiar el carrito de la sesión después de completar el pedido
            session.pop('carrito', None)
            flash('Pedido realizado con éxito', 'success')

            # Enviar notificación al administrador
            usuario_nombre = session.get('usuario_nombre', 'Un usuario')
            mensaje = f'El usuario "{usuario_nombre}" acaba de realizar una compra por S/. {total:.2f}'
            controlador_notificaciones.agregar_notificacion(usuario_id, pedido_id, mensaje)

            if 'usuario_tipo' in session and session['usuario_tipo'] == 'administrador':
                flash('Alguien realizó una compra!', 'notification')

            # Redirigir a la página de confirmación del pedido
            return redirect(url_for('confirmacion_pedido', pedido_id=pedido_id))

    except Exception as e:
        # Manejo de errores generales
        app.logger.error(f'Error inesperado al realizar el pedido: {str(e)}')
        flash('Ocurrió un error inesperado al realizar tu pedido. Por favor, inténtalo nuevamente.', 'error')
        return redirect(url_for('realizar_pedido'))

    # Si es una solicitud GET, mostrar la página para seleccionar la dirección de envío
    try:
        direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
        metodos_pago = controlador_metodo_pago.listar_metodos_pago(session['usuario_id'])
    except Exception as e:
        app.logger.error(f'Error al obtener datos del usuario: {str(e)}')
        flash('Ocurrió un error al cargar tus datos. Por favor, inténtalo nuevamente.', 'error')
        return redirect(url_for('home'))

    # Calcular el total del pedido para mostrarlo en la página
    total = 0
    if 'carrito' in session:
        for item in session['carrito']:
            try:
                total += int(item['cantidad']) * float(item['precio'])
            except (ValueError, TypeError) as calc_error:
                app.logger.error(f'Error al calcular el total del carrito: {str(calc_error)}')
                flash('Ocurrió un error al calcular el total del carrito. Por favor, revisa los productos.', 'error')
                return redirect(url_for('carrito'))

    return render_template('realizar_pedido.html', direcciones=direcciones, metodos_pago=metodos_pago, total=total)

@app.route('/pedido/<int:pedido_id>', methods=['GET'])
@login_required
def detalle_pedido(pedido_id):
    pedido = controlador_pedido.obtener_pedido_por_id(pedido_id)

    if not pedido:
        flash('El pedido no existe.', 'error')
        return redirect(url_for('mis_pedidos'))

    if pedido['usuario_id'] != session['usuario_id']:
        flash('No tienes permiso para ver este pedido.', 'error')
        return redirect(url_for('mis_pedidos'))

    return render_template('detalle_pedido.html', pedido=pedido)

@app.route('/confirmacion-pedido/<int:pedido_id>')
@login_required
def confirmacion_pedido(pedido_id):
    pedido = controlador_pedido.obtener_pedido_por_id(pedido_id)
    if not pedido or pedido['usuario_id'] != session['usuario_id']:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('home'))
    return render_template('confirmacion_pedido.html', pedido=pedido)

@app.route('/mis-pedidos')
@login_required
def mis_pedidos():
    pedidos = controlador_pedido.obtener_pedidos_por_usuario(session['usuario_id'])
    return render_template('mis_pedidos.html', pedidos=pedidos)

@app.route('/producto/<int:id>/opiniones', methods=['POST'])
@login_required
def agregar_opiniones(id):
    calificacion = int(request.form.get('calificacion'))
    comentario = request.form.get('comentario')
    usuario_id = session['usuario_id']

    controlador_opinion.agregar_opiniones(id, usuario_id, comentario, calificacion)
    flash('Reseña agregada con éxito', 'success')
    return redirect(url_for('producto', id=id))

@app.route('/mi-cuenta')
@login_required
def mi_cuenta():
    usuario_id = session.get('usuario_id')
    usuario = controlador_usuario.obtener_usuario_por_id(usuario_id)
    return render_template('mi_cuenta.html', usuario=usuario)

@app.route('/mis-metodos-pago')
@login_required
def mis_metodos_pago():
    metodos = controlador_metodo_pago.listar_metodos_pago(session['usuario_id'])
    return render_template('metodos_pago.html', metodos=metodos)

@app.route('/agregar-metodo-pago', methods=['GET', 'POST'])
@login_required
def agregar_metodo_pago():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        numero_tarjeta = request.form.get('numero_tarjeta')
        titular = request.form.get('titular')
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        cvv = request.form.get('cvv')
        predeterminado = bool(request.form.get('predeterminado'))

        metodo = MetodoPago(
            usuario_id=session['usuario_id'],
            tipo=tipo,
            numero_tarjeta=numero_tarjeta,
            titular=titular,
            fecha_vencimiento=fecha_vencimiento,
            cvv=cvv,
            predeterminado=predeterminado
        )
        
        try:
            controlador_metodo_pago.insertar_metodo_pago(metodo)
            flash('Método de pago agregado correctamente', 'success')
            return redirect(url_for('mis_metodos_pago'))
        except Exception as e:
            flash('Error al agregar el método de pago', 'error')
            return redirect(url_for('agregar_metodo_pago'))
            
    return render_template('agregar_metodo_pago.html')

@app.route('/editar-metodo-pago/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_metodo_pago(id):
    metodo = controlador_metodo_pago.obtener_metodo_pago(id)
    if not metodo or metodo['usuario_id'] != session['usuario_id']:
        flash('Método de pago no encontrado', 'error')
        return redirect(url_for('mis_metodos_pago'))
    
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        titular = request.form.get('titular')
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        predeterminado = bool(request.form.get('predeterminado'))

        metodo_actualizado = MetodoPago(
            id=id,
            usuario_id=session['usuario_id'],
            tipo=tipo,
            titular=titular,
            fecha_vencimiento=fecha_vencimiento,
            predeterminado=predeterminado
        )
        
        try:
            controlador_metodo_pago.actualizar_metodo_pago(id, metodo_actualizado)
            flash('Método de pago actualizado correctamente', 'success')
            return redirect(url_for('mis_metodos_pago'))
        except Exception as e:
            flash('Error al actualizar el método de pago', 'error')
            
    return render_template('editar_metodo_pago.html', metodo=metodo)

@app.route('/eliminar-metodo-pago/<int:id>', methods=['POST'])
@login_required
def eliminar_metodo_pago(id):
    metodo = controlador_metodo_pago.obtener_metodo_pago(id)
    if not metodo or metodo['usuario_id'] != session['usuario_id']:
        flash('Método de pago no encontrado', 'error')
        return redirect(url_for('mis_metodos_pago'))
    
    try:
        controlador_metodo_pago.eliminar_metodo_pago(id)
        flash('Método de pago eliminado correctamente', 'success')
    except Exception as e:
        flash('Error al eliminar el método de pago', 'error')
        
    return redirect(url_for('mis_metodos_pago'))

@app.route('/establecer-metodo-pago-predeterminado/<int:id>', methods=['POST'])
@login_required
def establecer_metodo_pago_predeterminado(id):
    metodo = controlador_metodo_pago.obtener_metodo_pago(id)
    if not metodo or metodo['usuario_id'] != session['usuario_id']:
        flash('Método de pago no encontrado', 'error')
        return redirect(url_for('mis_metodos_pago'))
    
    try:
        controlador_metodo_pago.establecer_predeterminado(id, session['usuario_id'])
        flash('Método de pago establecido como predeterminado', 'success')
    except Exception as e:
        flash('Error al establecer el método de pago como predeterminado', 'error')
        
    return redirect(url_for('mis_metodos_pago'))

@app.route('/actualizar-cuenta', methods=['POST'])
@login_required
def actualizar_cuenta():
    usuario_id = session.get('usuario_id')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')

    usuario = controlador_usuario.obtener_usuario_por_id(usuario_id)
    tipo = usuario.tipo

    foto = request.files.get('foto')
    if foto:
        foto_filename = secure_filename(foto.filename)
        foto.save(os.path.join(UPLOAD_FOLDER, foto_filename))
    else:
        foto_filename = usuario.foto

    controlador_usuario.actualizar_usuario(usuario_id, nombre, apellido, email, tipo, foto_filename)
    # Redirigir a la página de direcciones
    session['usuario_nombre'] = nombre.split()[0] if nombre else ""
    session['usuario_apellido'] = apellido.split()[0] if apellido else ""
    flash('Tu cuenta ha sido actualizada exitosamente', 'success')
    return redirect(url_for('mi_cuenta'))

@app.route('/acerca-de')
def acerca_de():
    return render_template('acerca_de.html')

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')

@app.route('/enviar_contacto', methods=['POST'])
def enviar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    flash('Tu mensaje ha sido enviado exitosamente. Te contactaremos pronto.', 'success')
    return redirect(url_for('contactanos'))

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/cambiar-contrasena', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena():
    if request.method == 'POST':
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']
        
        usuario = controlador_usuario.obtener_usuario_por_id(session['usuario_id'])
        if check_password_hash(usuario.contrasena, contrasena_actual):
            if nueva_contrasena == confirmar_contrasena:
                hashed_password = generate_password_hash(nueva_contrasena)
                controlador_usuario.actualizar_contrasena(session['usuario_id'], hashed_password)
                flash('contrasena actualizada correctamente', 'success')
                return redirect(url_for('mi_cuenta'))
            else:
                flash('Las contrasenas nuevas no coinciden', 'error')
        else:
            flash('La contrasena actual es incorrecta', 'error')
    
    return render_template('cambiar_contrasena.html')

# Rutas del Blueprint de administración
@admin_bp.route('/')
@admin_required
def admin_dashboard():
    total_productos = controlador_producto.contar_productos()
    pedidos_pendientes = controlador_pedido.contar_pedidos_pendientes()
    total_usuarios = controlador_usuario.contar_usuarios()
    ingresos_mes = controlador_pedido.calcular_ingresos_mes()
    notificaciones = controlador_notificaciones.obtener_notificaciones()
    return render_template('admin/dashboard.html', 
                           total_productos=total_productos,
                           pedidos_pendientes=pedidos_pendientes,
                           total_usuarios=total_usuarios,
                           ingresos_mes=ingresos_mes,
                           notificaciones=notificaciones)

@admin_bp.route('/productos')
@admin_required
def admin_productos():
    productos = controlador_producto.obtener_todos_productos()
    return render_template('admin/productos.html', productos=productos)

@admin_bp.route('/nuevo_producto', methods=['GET', 'POST'])
@admin_required
def admin_nuevo_producto():
    categorias = controlador_categorias.obtener_todas_categorias()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        destacado = 1 if 'destacado' in request.form else 0

        # Verificar si se subió una imagen
        if 'imagen' not in request.files:
            flash('La imagen es obligatoria', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias)

        imagen = request.files['imagen']
        if imagen.filename == '':
            flash('Debe seleccionar una imagen', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias)

        if not allowed_file(imagen.filename):
            flash('Formato de imagen no permitido. Use: png, jpg, jpeg, gif', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias)

        try:
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))

            controlador_producto.insertar_producto(
                nombre=nombre,
                descripcion=descripcion,
                categoria_id=categoria_id,
                precio=precio,
                stock=stock,
                destacado=destacado,
                imagen=imagen_filename
            )
            flash('Producto creado con éxito', 'success')
            return redirect(url_for('admin.admin_productos'))

        except Exception as e:
            if imagen_filename:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, imagen_filename))
                except Exception:
                    pass
            flash(f'Error al crear el producto: {str(e)}', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias)

    return render_template('admin/editar_nuevo_producto.html', producto=None, categorias=categorias)

@admin_bp.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    categorias = controlador_categorias.obtener_todas_categorias()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        destacado = 1 if 'destacado' in request.form else 0

        imagen = request.files['imagen']
        imagen_filename = producto.imagen
        
        if imagen and allowed_file(imagen.filename):
            try:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            except Exception as e:
                flash(f'Error al cargar la imagen: {str(e)}', 'error')
                return redirect(url_for('admin.admin_editar_producto', id=id))

        try:
            controlador_producto.actualizar_producto(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                categoria_id=categoria_id,
                imagen=imagen_filename
            )
            flash('Producto actualizado con éxito', 'success')
        except Exception as e:
            flash(f'Error al actualizar el producto: {str(e)}', 'error')

        return redirect(url_for('admin.admin_productos'))

    return render_template('admin/editar_nuevo_producto.html', producto=producto, categorias=categorias)

@admin_bp.route('/producto/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_producto(id):
    try:
        controlador_producto.eliminar_producto(id)
        flash('Producto eliminado con éxito', 'success')
    except IntegrityError as e:
        if e.args[0] == 1451:
            flash('No se puede eliminar el producto porque está relacionado con un pedido.', 'error')
        else:
            flash(f'Ocurrió un error al eliminar el producto: {str(e)}', 'error')
    except Exception as e:
        flash(f'Ocurrió un error inesperado: {str(e)}', 'error')
    return redirect(url_for('admin.admin_productos'))

@admin_bp.route('/pedidos')
@admin_required
def admin_pedidos():
    pedidos = controlador_pedido.obtener_todos_pedidos()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@admin_bp.route('/pedido/<int:id>', methods=['GET'])
@admin_required
def admin_detalle_pedido(id):
    pedido = controlador_pedido.obtener_pedido_por_id(id)
    if not pedido:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('admin.admin_pedidos'))
    return render_template('admin/detalle_pedido.html', pedido=pedido)

@admin_bp.route('/pedido/actualizar-estado/<int:id>', methods=['POST'])
@admin_required
def admin_actualizar_estado_pedido(id):
    nuevo_estado = request.form.get('nuevo_estado')
    controlador_pedido.actualizar_estado_pedido(id, nuevo_estado)
    flash('Estado del pedido actualizado con éxito', 'success')
    return redirect(url_for('admin.admin_pedidos'))

@admin_bp.route('/pedido/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_pedido(id):
    pedido = controlador_pedido.obtener_pedido_por_id(id)
    
    if request.method == 'POST':
        calle = request.form.get('calle')
        ciudad = request.form.get('ciudad')
        estado = request.form.get('estado')
        pais = request.form.get('pais')
        fecha_pedido = request.form.get('fecha_pedido')
        estado_pedido = request.form.get('estado_pedido')

        if calle and ciudad and estado and pais and fecha_pedido and estado_pedido:
            try:
                controlador_pedido.editar_pedido(id, calle, ciudad, estado, pais, fecha_pedido, estado_pedido)
                flash('Pedido actualizado con éxito', 'success')
                return redirect(url_for('admin.admin_pedidos'))
            except Exception as e:
                flash(f'Error al actualizar el pedido: {str(e)}', 'error')
        else:
            flash('Faltan campos por completar', 'error')
    
    return render_template('admin/editar_pedido.html', pedido=pedido)

@admin_bp.route('/pedido/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_pedido(id):
    try:
        # Intentamos eliminar el pedido
        if controlador_pedido.eliminar_pedido(id):
            flash('Pedido eliminado con éxito.', 'success')
        else:
            flash('No se pudo eliminar el pedido. Verifique que no tenga registros asociados.', 'error')
            
    except IntegrityError as e:
        logger.error(f"Error de integridad al eliminar pedido {id}: {str(e)}")
        if e.args[0] == 1451:
            flash('No se puede eliminar el pedido porque está relacionado con otros registros.', 'error')
        else:
            flash('Error de integridad en la base de datos.', 'error')
            
    except Exception as e:
        logger.error(f"Error inesperado al eliminar pedido {id}: {str(e)}")
        flash('Ocurrió un error inesperado al intentar eliminar el pedido.', 'error')
        
    return redirect(url_for('admin.admin_pedidos'))

@admin_bp.route('/categorias')
@admin_required
def admin_categorias():
    try:
        categorias = controlador_categorias.obtener_todas_categorias()
        if not categorias:
            flash('No se encontraron categorías o hubo un error al cargarlas.', 'warning')
            categorias = []
        
        for categoria in categorias:
            categoria['productos_count'] = controlador_categorias.contar_productos_por_categoria(categoria['id'])
            
        return render_template('admin/categorias.html', categorias=categorias)
    except Exception as e:
        flash('Ocurrió un error al cargar las categorías.', 'error')
        return render_template('admin/categorias.html', categorias=[])

@admin_bp.route('/categorias/nueva', methods=['GET', 'POST'])
@admin_required
def admin_nueva_categorias():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash('El nombre de la categoría es obligatorio', 'error')
            return render_template('admin/editar_nueva_categorias.html', categorias=None)
        
        try:
            controlador_categorias.insertar_categorias(nombre)
            flash('Categoría creada con éxito', 'success')
            return redirect(url_for('admin.admin_categorias'))
        except Exception as e:
            flash(f'Error al crear la categoría: {str(e)}', 'error')
            return render_template('admin/editar_nueva_categorias.html', categorias=None)
            
    return render_template('admin/editar_nueva_categorias.html', categorias=None)

@admin_bp.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_categorias(id):
    categorias = controlador_categorias.obtener_categorias_por_id(id)
    if not categorias:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('admin.admin_categorias'))
        
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash('El nombre de la categoría es obligatorio', 'error')
            return render_template('admin/editar_nueva_categorias.html', categorias=categorias)
            
        try:
            controlador_categorias.actualizar_categorias(id, nombre)
            flash('Categoría actualizada con éxito', 'success')
            return redirect(url_for('admin.admin_categorias'))
        except Exception as e:
            flash(f'Error al actualizar la categoría: {str(e)}', 'error')
            return render_template('admin/editar_nueva_categorias.html', categorias=categorias)
            
    return render_template('admin/editar_nueva_categorias.html', categorias=categorias)

@admin_bp.route('/categorias/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_categorias(id):
    try:
        if controlador_categorias.eliminar_categorias(id):
            flash('Categoría eliminada con éxito.', 'success')
        else:
            flash('No se pudo eliminar la categoría. Verifique que no tenga productos asociados.', 'error')
            
    except IntegrityError as e:
        logger.error(f"Error de integridad al eliminar categoría {id}: {str(e)}")
        if e.args[0] == 1451:  # Código de error de clave foránea
            flash('No se puede eliminar la categoría porque está asociada a productos.', 'error')
        else:
            flash('Error de integridad en la base de datos.', 'error')
            
    except Exception as e:
        logger.error(f"Error inesperado al eliminar categoría {id}: {str(e)}")
        flash('Ocurrió un error inesperado al intentar eliminar la categoría.', 'error')
        
    return redirect(url_for('admin.admin_categorias'))

@admin_bp.route('/usuarios')
@admin_required
def admin_usuarios():
    usuarios = controlador_usuario.obtener_todos_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuario/<int:id>/detalle', methods=['GET'])
@admin_required
def admin_detalle_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template('admin/detalle_usuario.html', usuario=usuario)

@admin_bp.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        tipo = request.form['tipo']
        nueva_contrasena = request.form.get('contrasena')
        
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):
            try:
                filename = secure_filename(foto.filename)
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(foto_path)
            except Exception as e:
                flash('Error al subir la imagen: ' + str(e), 'error')
                return redirect(url_for('admin.admin_editar_usuario', id=id))
        else:
            filename = usuario.foto

        controlador_usuario.actualizar_usuario(
            id=id,
            nombre=nombre,
            apellido=apellido,
            email=email,
            tipo=tipo,
            foto=filename,
            nueva_contrasena=nueva_contrasena if nueva_contrasena else None
        )

        flash('Usuario actualizado con éxito', 'success')
        return redirect(url_for('admin.admin_usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario)

@admin_bp.route('/usuario/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_usuario(id):
    try:
        if controlador_usuario.tiene_pedidos_pendientes(id):
            flash('No se puede eliminar este usuario, ya que tiene pedidos pendientes', 'error')
            return redirect(url_for('admin.admin_usuarios'))
            
        controlador_usuario.eliminar_usuario(id)
        flash('Usuario eliminado con éxito', 'success')
        
    except IntegrityError as e:
        logger.error(f"Error de integridad al eliminar usuario {id}: {str(e)}")
        flash('No se puede eliminar este usuario, ya que tiene pedidos pendientes', 'error')
        
    except Exception as e:
        logger.error(f"Error al eliminar usuario {id}: {str(e)}")
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')
        
    return redirect(url_for('admin.admin_usuarios'))

# Notificaciones PUSH
@admin_bp.route('/notificaciones', methods=['GET'])
@admin_required
def obtener_notificaciones():
    try:
        notificaciones = controlador_notificaciones.obtener_notificaciones()
        return jsonify(notificaciones)
    except Exception as e:
        return jsonify([]), 500

@admin_bp.route('/notificaciones/marcar_vista', methods=['POST'])
@admin_required
def marcar_notificacion_vista():
    try:
        notificacion_id = request.form.get('notificacion_id')
        if not notificacion_id:
            return jsonify({'success': False, 'error': 'ID de notificación requerido'}), 400
            
        resultado = controlador_notificaciones.marcar_notificacion_como_vista(notificacion_id)
        if resultado:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'No se pudo actualizar la notificación'}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/obtener-notificaciones-recientes')
def obtener_notificaciones_recientes():
    if session.get('usuario_tipo') != 'administrador':
        return jsonify([])

    notificaciones = controlador_notificaciones.obtener_notificaciones_recientes()
    return jsonify(notificaciones)

app.register_blueprint(admin_bp)

#APIS
@app.route('/api/ubicacion/paises', methods=['GET'])
def obtener_paises():
    try:
        paises = controlador_ubicacion.obtener_todos_paises()
        return jsonify(paises)  
    except Exception as e:
        logger.error(f"Error al obtener países: {str(e)}")
        return jsonify({'error': 'Error al obtener países'}), 500

@app.route('/api/ubicacion/estados/<int:pais_id>', methods=['GET'])
def obtener_estados(pais_id):
    try:
        estados = controlador_ubicacion.obtener_estados_por_pais(pais_id)
        return jsonify(estados)
    except Exception as e:
        logger.error(f"Error al obtener estados: {str(e)}")
        return jsonify({'error': 'Error al obtener estados'}), 500

@app.route('/api/ubicacion/ciudades/<int:estado_id>', methods=['GET'])
def obtener_ciudades(estado_id):
    try:
        ciudades = controlador_ubicacion.obtener_ciudades_por_estado(estado_id)
        return jsonify(ciudades)
    except Exception as e:
        logger.error(f"Error al obtener ciudades: {str(e)}")
        return jsonify({'error': 'Error al obtener ciudades'}), 500

@app.route('/api/ubicacion/distritos/<int:ciudad_id>', methods=['GET'])
def obtener_distritos(ciudad_id):
    try:
        distritos = controlador_ubicacion.obtener_distritos_por_ciudad(ciudad_id)
        return jsonify(distritos)
    except Exception as e:
        logger.error(f"Error al obtener distritos: {str(e)}")
        return jsonify({'error': 'Error al obtener distritos'}), 500

@app.route('/api/direccion/geocodificar', methods=['POST'])
@login_required
def geocodificar_direccion():
    try:
        datos = request.get_json()
        if not datos or 'direccion' not in datos:
            raise BadRequest('Dirección requerida')

        resultado = controlador_direcciones.geocodificar_direccion(datos['direccion'])
        if resultado:
            return jsonify(resultado)
        return jsonify({'error': 'No se pudo geocodificar la dirección'}), 400
    except Exception as e:
        logger.error(f"Error en geocodificación: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)