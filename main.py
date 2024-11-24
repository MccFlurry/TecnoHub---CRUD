from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
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
from controllers import controlador_direcciones
from controllers import controlador_usuario
from controllers import controlador_producto
from controllers import controlador_pedido
from controllers import controlador_kit
from controllers import controlador_favorito
from controllers import controlador_opinion
from controllers import controlador_notificaciones
from controllers import controlador_ubicacion
from controllers import controlador_metodo_pago
from controllers import controlador_marca
from controllers import controlador_modelo
from controllers import controlador_categorias
import datetime

app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key = 'tu_clave_secreta'

# Configuración JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'tu-clave-jwt-secreta')  # Mejor usar variable de entorno
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Dónde buscar el token
app.config['JWT_HEADER_NAME'] = 'Authorization'  # Nombre del header
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Tipo de token
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'  # Clave para mensajes de error

jwt = JWTManager(app)

# Manejadores de errores JWT
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'El token ha expirado',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Verificación de token fallida',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': 'No se proporcionó token de acceso',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Se requiere un token fresco para esta operación',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'El token ha sido revocado',
        'error': 'token_revoked'
    }), 401

# Configuración de carga de archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Verifica si la extensión del archivo está permitida
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración de rutas de archivos
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # Estamos en PythonAnywhere
    UPLOAD_FOLDER = '/home/Grupo5DAW/TecnoHub---CRUD/static/img'
else:
    # Estamos en desarrollo local
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img')

# Asegurarse de que el directorio de carga existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configurar Flask para usar el UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

logger = logging.getLogger(__name__)

# Agregar la configuración de CSRF para evitar el KeyError
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
app.config['WTF_CSRF_FIELD_NAME'] = 'csrf_token'
app.config['WTF_CSRF_HEADERS'] = ['X-CSRF-Token', 'X-CSRFToken', 'X-XSRF-Token']
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SSL_STRICT'] = False  # CLAVE PARA PYTHONANYWHERE
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

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
            direccion = request.form.get('direccion')
            ciudad_id = request.form.get('ciudad_id')
            estado_id = request.form.get('estado_id')
            pais_id = request.form.get('pais_id')
            codigo_postal = request.form.get('codigo_postal')
            distrito_id = request.form.get('distrito_id')  # Agregado distrito_id
            
            campos_requeridos = ['direccion', 'ciudad_id', 'estado_id', 'pais_id', 'codigo_postal', 'distrito_id']
            if not all(request.form.get(campo) for campo in campos_requeridos):
                flash('Por favor complete todos los campos requeridos.', 'error')
                return redirect(url_for('agregar_direccion'))

            usuario_id = session.get('usuario_id')
            
            controlador_direcciones.agregar_direccion(
                usuario_id=usuario_id,
                direccion=direccion,
                ciudad_id=ciudad_id,
                estado_id=estado_id,
                pais_id=pais_id,
                codigo_postal=codigo_postal,
                distrito_id=distrito_id  # Agregado distrito_id
            )
            
            flash('Dirección agregada con éxito', 'success')
            return redirect(url_for('mis_direcciones'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('agregar_direccion'))
        except Exception as e:
            flash('Error al agregar la dirección', 'error')
            return redirect(url_for('agregar_direccion'))

    try:
        paises = controlador_ubicacion.obtener_todos_paises()
        return render_template('agregar_direccion.html', paises=paises)
    except Exception as e:
        flash('Error al cargar los datos de ubicación', 'error')
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
            datos = {
                'direccion': request.form.get('direccion'),
                'ciudad_id': request.form.get('ciudad_id'),
                'estado_id': request.form.get('estado_id'),
                'pais_id': request.form.get('pais_id'),
                'codigo_postal': request.form.get('codigo_postal'),
                'distrito_id': request.form.get('distrito_id')  # Agregado distrito_id
            }

            campos_requeridos = ['direccion', 'ciudad_id', 'estado_id', 'pais_id', 'codigo_postal', 'distrito_id']
            if not all(datos.get(campo) for campo in campos_requeridos):
                flash('Por favor complete todos los campos requeridos.', 'error')
                return redirect(url_for('editar_direccion', direccion_id=direccion_id))

            controlador_direcciones.actualizar_direccion(direccion_id, datos)
            flash('Dirección actualizada con éxito', 'success')
            return redirect(url_for('mis_direcciones'))

        # GET: Obtener datos para los combo boxes
        paises = controlador_ubicacion.obtener_todos_paises()
        estados = controlador_ubicacion.obtener_estados_por_pais(direccion['pais_id']) if direccion.get('pais_id') else []
        ciudades = controlador_ubicacion.obtener_ciudades_por_estado(direccion['estado_id']) if direccion.get('estado_id') else []
        distritos = controlador_ubicacion.obtener_distritos_por_ciudad(direccion['ciudad_id']) if direccion.get('ciudad_id') else []
        
        return render_template('editar_direccion.html', 
                             direccion=direccion,
                             paises=paises,
                             estados=estados,
                             ciudades=ciudades,
                             distritos=distritos)

    except Exception as e:
        flash(f'Error al procesar la dirección: {str(e)}', 'error')
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
    query = request.args.get('q', '')
    categoria_id = request.args.get('categoria', type=int)
    marca_id = request.args.get('marca', type=int)
    modelo_id = request.args.get('modelo', type=int)
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)

    productos = controlador_producto.busqueda_avanzada(
        query=query,
        categoria_id=categoria_id,
        precio_min=precio_min,
        precio_max=precio_max,
        id_marca=marca_id,
        id_modelo=modelo_id
    )
    
    categorias = controlador_categorias.obtener_todas_categorias()
    marcas = controlador_marca.obtener_marcas()
    modelos = controlador_modelo.obtener_modelos()
    
    return render_template('resultados_busqueda.html',
                         productos=productos,
                         query=query,
                         categoria_seleccionada=categoria_id,
                         marca_seleccionada=marca_id,
                         modelo_seleccionado=modelo_id,
                         precio_min=precio_min,
                         precio_max=precio_max,
                         categorias=categorias,
                         marcas=marcas,
                         modelos=modelos)

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
            if 'carrito' not in session or not session['carrito']:
                flash('Tu carrito está vacío', 'error')
                return redirect(url_for('carrito'))

            direccion_id = request.form.get('direccion_id')
            if not direccion_id:
                flash('Debes seleccionar una dirección de envío', 'error')
                return redirect(url_for('realizar_pedido'))

            metodo_pago_id = request.form.get('metodo_pago_id')

            usuario_id = session.get('usuario_id')
            if not usuario_id:
                flash('No se pudo identificar al usuario. Por favor, inicia sesión nuevamente.', 'error')
                return redirect(url_for('login'))

            # Verificar stock antes de crear el pedido
            for item in session['carrito']:
                producto_id = item.get('producto_id')
                cantidad = int(item.get('cantidad'))
                stock_actual = controlador_producto.obtener_stock(producto_id)
                
                if stock_actual is None:
                    flash(f'El producto {item.get("nombre")} ya no está disponible', 'error')
                    return redirect(url_for('carrito'))
                    
                if stock_actual < cantidad:
                    flash(f'Stock insuficiente para {item.get("nombre")}. Stock disponible: {stock_actual}', 'error')
                    return redirect(url_for('carrito'))

            # Crear el pedido
            pedido_id = controlador_pedido.crear_pedido(
                usuario_id=usuario_id,
                direccion_id=int(direccion_id),
                metodo_pago_id=int(metodo_pago_id) if metodo_pago_id else None
            )
            
            total = 0
            # Procesar cada item del carrito
            for item in session['carrito']:
                try:
                    producto_id = item.get('producto_id')
                    cantidad = int(item.get('cantidad'))
                    precio = float(item.get('precio'))

                    # Actualizar stock (usando cantidad positiva para reducir)
                    if not controlador_producto.actualizar_stock(producto_id, cantidad):
                        raise Exception(f'No se pudo actualizar el stock del producto {item.get("nombre")}')

                    controlador_pedido.agregar_detalle_pedido(pedido_id, producto_id, cantidad, precio)
                    total += cantidad * precio

                except Exception as detalle_error:
                    app.logger.error(f'Error al procesar producto en pedido: {str(detalle_error)}')
                    flash('Ocurrió un error al procesar tu pedido', 'error')
                    return redirect(url_for('realizar_pedido'))

            session.pop('carrito', None)
            flash('Pedido realizado con éxito', 'success')

            usuario_nombre = session.get('usuario_nombre', 'Un usuario')
            mensaje = f'El usuario "{usuario_nombre}" acaba de realizar una compra por S/. {total:.2f}'
            controlador_notificaciones.agregar_notificacion(usuario_id, pedido_id, mensaje)

            if 'usuario_tipo' in session and session['usuario_tipo'] == 'administrador':
                flash('Alguien realizó una compra!', 'notification')

            return redirect(url_for('confirmacion_pedido', pedido_id=pedido_id))

    except Exception as e:
        app.logger.error(f'Error inesperado al realizar el pedido: {str(e)}')
        flash('Ocurrió un error inesperado al realizar tu pedido. Por favor, inténtalo nuevamente.', 'error')
        return redirect(url_for('realizar_pedido'))

    try:
        direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
        metodos_pago = controlador_metodo_pago.listar_metodos_pago(session['usuario_id'])
    except Exception as e:
        app.logger.error(f'Error al obtener datos del usuario: {str(e)}')
        flash('Ocurrió un error al cargar tus datos. Por favor, inténtalo nuevamente.', 'error')
        return redirect(url_for('home'))

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

        metodo = controlador_metodo_pago.MetodoPago(
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

        metodo_actualizado = controlador_metodo_pago.MetodoPago(
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
        if controlador_usuario.check_password(usuario.contrasena, contrasena_actual):
            if nueva_contrasena == confirmar_contrasena:
                hashed_password = controlador_usuario.generate_password_hash(nueva_contrasena)
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
    marcas = controlador_marca.obtener_marcas()
    modelos = controlador_modelo.obtener_modelos()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        id_marca = request.form.get('id_marca')  # Puede ser None
        id_modelo = request.form.get('id_modelo')  # Puede ser None
        destacado = 1 if 'destacado' in request.form else 0

        imagen = request.files['imagen']
        if imagen.filename == '':
            flash('Debe seleccionar una imagen', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias,
                                marcas=marcas,
                                modelos=modelos)

        if not allowed_file(imagen.filename):
            flash('Formato de imagen no permitido. Use: png, jpg, jpeg, gif', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=None, 
                                categorias=categorias,
                                marcas=marcas,
                                modelos=modelos)

        try:
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))

            controlador_producto.insertar_producto(
                nombre=nombre,
                descripcion=descripcion,
                categoria_id=categoria_id,
                precio=precio,
                stock=stock,
                id_marca=id_marca,
                id_modelo=id_modelo,
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
                                categorias=categorias,
                                marcas=marcas,
                                modelos=modelos)

    return render_template('admin/editar_nuevo_producto.html', 
                         producto=None, 
                         categorias=categorias,
                         marcas=marcas,
                         modelos=modelos)

@admin_bp.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    categorias = controlador_categorias.obtener_todas_categorias()
    marcas = controlador_marca.obtener_marcas()
    modelos = controlador_modelo.obtener_modelos()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        id_marca = request.form.get('id_marca')  # Puede ser None
        id_modelo = request.form.get('id_modelo')  # Puede ser None
        destacado = 1 if 'destacado' in request.form else 0

        imagen = request.files['imagen']
        imagen_filename = producto.imagen
        
        if imagen and allowed_file(imagen.filename):
            try:
                if producto.imagen:
                    try:
                        os.remove(os.path.join(UPLOAD_FOLDER, producto.imagen))
                    except Exception:
                        pass
                
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            except Exception as e:
                flash(f'Error al guardar la imagen: {str(e)}', 'error')
                return render_template('admin/editar_nuevo_producto.html', 
                                    producto=producto,
                                    categorias=categorias,
                                    marcas=marcas,
                                    modelos=modelos)

        try:
            controlador_producto.actualizar_producto(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                categoria_id=categoria_id,
                precio=precio,
                stock=stock,
                id_marca=id_marca,
                id_modelo=id_modelo,
                imagen=imagen_filename
            )
            flash('Producto actualizado con éxito', 'success')
            return redirect(url_for('admin.admin_productos'))
        except Exception as e:
            flash(f'Error al actualizar el producto: {str(e)}', 'error')
            return render_template('admin/editar_nuevo_producto.html', 
                                producto=producto,
                                categorias=categorias,
                                marcas=marcas,
                                modelos=modelos)

    return render_template('admin/editar_nuevo_producto.html', 
                         producto=producto,
                         categorias=categorias,
                         marcas=marcas,
                         modelos=modelos)

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
        if controlador_pedido.eliminar_pedido(id):
            flash('Pedido eliminado con éxito.', 'success')
        else:
            flash('No se pudo eliminar el pedido. Verifique que no tenga registros asociados.', 'error')
            
    except IntegrityError as e:
        logger.error(f"Error de integridad al eliminar pedido {id}: {str(e)}")
        if e.args[0] == 1451:  # Código de error de clave foránea
            flash('No se puede eliminar el pedido porque está relacionado con otros registros.', 'error')
        else:
            flash('Error de integridad en la base de datos.', 'error')
            
    except Exception as e:
        logger.error(f"Error al eliminar pedido {id}: {str(e)}")
        flash(f'Error al eliminar el pedido: {str(e)}', 'error')
        
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

# Rutas para Marcas
@admin_bp.route('/marcas')
@admin_required
def admin_marcas():
    marcas = controlador_marca.obtener_marcas()
    return render_template('admin/marcas.html', marcas=marcas)

@admin_bp.route('/marcas/nueva', methods=['GET', 'POST'])
@admin_required
def admin_nueva_marca():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            marca = controlador_marca.Marca(nombre=nombre)
            controlador_marca.insertar_marca(marca)
            flash('Marca agregada exitosamente', 'success')
            return redirect(url_for('admin.admin_marcas'))
        except Exception as e:
            flash(f'Error al agregar la marca: {str(e)}', 'error')
    return render_template('admin/editar_nueva_marca.html', marca=None)

@admin_bp.route('/marcas/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_marca(id):
    marca = controlador_marca.obtener_marca_por_id(id)
    if not marca:
        flash('Marca no encontrada', 'error')
        return redirect(url_for('admin.admin_marcas'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            controlador_marca.actualizar_marca(id, nombre)
            flash('Marca actualizada exitosamente', 'success')
            return redirect(url_for('admin.admin_marcas'))
        except Exception as e:
            flash(f'Error al actualizar la marca: {str(e)}', 'error')
    
    return render_template('admin/editar_nueva_marca.html', marca=marca)

@admin_bp.route('/marcas/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_marca(id):
    try:
        controlador_marca.eliminar_marca(id)
        flash('Marca eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la marca: {str(e)}', 'error')
    return redirect(url_for('admin.admin_marcas'))

# Rutas para Modelos
@admin_bp.route('/modelos')
@admin_required
def admin_modelos():
    modelos = controlador_modelo.obtener_modelos()
    return render_template('admin/modelos.html', modelos=modelos)

@admin_bp.route('/modelos/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_nuevo_modelo():
    marcas = controlador_marca.obtener_marcas()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            modelo = controlador_modelo.Modelo(nombre=nombre)
            controlador_modelo.insertar_modelo(modelo)
            flash('Modelo agregado exitosamente', 'success')
            return redirect(url_for('admin.admin_modelos'))
        except Exception as e:
            flash(f'Error al agregar el modelo: {str(e)}', 'error')
    return render_template('admin/editar_nuevo_modelo.html', modelo=None, marcas=marcas)

@admin_bp.route('/modelos/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_modelo(id):
    modelo = controlador_modelo.obtener_modelo_por_id(id)
    marcas = controlador_marca.obtener_marcas()
    
    if not modelo:
        flash('Modelo no encontrado', 'error')
        return redirect(url_for('admin.admin_modelos'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            modelo.nombre = nombre
            controlador_modelo.actualizar_modelo(modelo)
            flash('Modelo actualizado exitosamente', 'success')
            return redirect(url_for('admin.admin_modelos'))
        except Exception as e:
            flash(f'Error al actualizar el modelo: {str(e)}', 'error')
    
    return render_template('admin/editar_nuevo_modelo.html', modelo=modelo, marcas=marcas)

@admin_bp.route('/modelos/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_modelo(id):
    try:
        controlador_modelo.eliminar_modelo(id)
        flash('Modelo eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el modelo: {str(e)}', 'error')
    return redirect(url_for('admin.admin_modelos'))

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

# JWT Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    # Verificar credenciales usando el controlador existente
    usuario = controlador_usuario.iniciar_sesion(email, password)
    
    if not usuario:
        return jsonify({"message": "Bad email or password"}), 401

    # Crear tokens de acceso y actualización
    access_token = create_access_token(
        identity=usuario['id'],
        additional_claims={
            'tipo': usuario['tipo'],
            'email': usuario['email']
        }
    )
    refresh_token = create_refresh_token(
        identity=usuario['id'],
        additional_claims={
            'tipo': usuario['tipo'],
            'email': usuario['email']
        }
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": usuario['id'],
        "user_type": usuario['tipo']
    })

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Endpoint para renovar el token de acceso usando el refresh token"""
    current_user_id = get_jwt_identity()
    usuario = controlador_usuario.obtener_usuario_por_id(current_user_id)
    
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    new_access_token = create_access_token(
        identity=current_user_id,
        additional_claims={
            'tipo': usuario.tipo,
            'email': usuario.email
        }
    )
    return jsonify({"access_token": new_access_token})

@app.route('/api/auth/verify', methods=['GET'])
@jwt_required()
def verify_token():
    current_user_id = get_jwt_identity()
    usuario = controlador_usuario.obtener_usuario_por_id(current_user_id)
    
    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404
        
    return jsonify({
        "user_id": current_user_id,
        "user_type": usuario.tipo,
        "email": usuario.email
    })

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    """Endpoint para cerrar sesión (en el futuro se puede implementar blacklisting de tokens)"""
    jti = get_jwt()['jti']
    # Aquí se podría agregar el token a una lista negra si se implementa
    return jsonify({"message": "Sesión cerrada exitosamente"})

#APIS
@app.route('/api/ubicacion/paises', methods=['GET'])
@jwt_required()
def obtener_paises():
    try:
        paises = controlador_ubicacion.obtener_paises()
        return jsonify({"status": "success", "data": paises}), 200
    except Exception as e:
        logger.error(f"Error al obtener países: {str(e)}")
        return jsonify({"status": "error", "message": "Error al obtener países"}), 500

@app.route('/api/ubicacion/estados/<int:pais_id>', methods=['GET'])
@jwt_required()
def obtener_estados(pais_id):
    try:
        estados = controlador_ubicacion.obtener_estados_por_pais(pais_id)
        return jsonify({"status": "success", "data": estados}), 200
    except Exception as e:
        logger.error(f"Error al obtener estados: {str(e)}")
        return jsonify({"status": "error", "message": "Error al obtener estados"}), 500

@app.route('/api/ubicacion/ciudades/<int:estado_id>', methods=['GET'])
@jwt_required()
def obtener_ciudades(estado_id):
    try:
        ciudades = controlador_ubicacion.obtener_ciudades_por_estado(estado_id)
        return jsonify({"status": "success", "data": ciudades}), 200
    except Exception as e:
        logger.error(f"Error al obtener ciudades: {str(e)}")
        return jsonify({"status": "error", "message": "Error al obtener ciudades"}), 500

@app.route('/api/ubicacion/distritos/<int:ciudad_id>', methods=['GET'])
@jwt_required()
def obtener_distritos(ciudad_id):
    try:
        distritos = controlador_ubicacion.obtener_distritos_por_ciudad(ciudad_id)
        return jsonify({"status": "success", "data": distritos}), 200
    except Exception as e:
        logger.error(f"Error al obtener distritos: {str(e)}")
        return jsonify({"status": "error", "message": "Error al obtener distritos", "error_detail": str(e)}), 500

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
        return jsonify({"status": "error", "message": "No se pudo geocodificar la dirección"}), 400
    except Exception as e:
        logger.error(f"Error en geocodificación: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Ubicación
@app.route('/api/estados/<int:pais_id>', methods=['GET'])
@jwt_required()
def api_obtener_estados(pais_id):
    try:
        estados = controlador_ubicacion.obtener_estados_por_pais(pais_id)
        return jsonify({"status": "success", "data": estados}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ciudades/<int:estado_id>', methods=['GET'])
@jwt_required()
def api_obtener_ciudades(estado_id):
    try:
        ciudades = controlador_ubicacion.obtener_ciudades_por_estado(estado_id)
        return jsonify({"status": "success", "data": ciudades}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/ubicacion/completa/<int:distrito_id>', methods=['GET'])
@jwt_required()
def obtener_ubicacion_completa_api(distrito_id):
    try:
        ubicacion = controlador_ubicacion.obtener_ubicacion_completa(distrito_id)
        if not ubicacion:
            return jsonify({"status": "error", "message": "Ubicación no encontrada"}), 404
        return jsonify({"status": "success", "data": ubicacion}), 200
    except Exception as e:
        logger.error(f"Error al obtener ubicación completa: {str(e)}")
        return jsonify({"status": "error", "message": "Error al obtener ubicación completa"}), 500

# APIs para Dirección
@app.route('/api/usuarios/<int:usuario_id>/direcciones', methods=['GET'])
@jwt_required()
def api_obtener_direcciones_usuario(usuario_id):
    try:
        direcciones = controlador_direcciones.obtener_direcciones_usuario(usuario_id)
        if not direcciones:
            return jsonify({"status": "success", "data": []}), 200
        return jsonify({"status": "success", "data": direcciones}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/direcciones/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_direccion(id):
    try:
        direccion = controlador_direcciones.obtener_direccion_por_id(id)
        if not direccion:
            return jsonify({"status": "error", "message": "Dirección no encontrada"}), 404
        return jsonify({"status": "success", "data": direccion}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/direcciones', methods=['POST'])
@jwt_required()
def api_crear_direccion():
    try:
        datos = request.get_json()
        required_fields = ['usuario_id', 'calle', 'numero', 'codigo_postal', 'ciudad_id', 'distrito_id']  # Agregado distrito_id
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        try:
            datos['usuario_id'] = int(datos['usuario_id'])
            datos['ciudad_id'] = int(datos['ciudad_id'])
            datos['distrito_id'] = int(datos['distrito_id'])  # Agregado distrito_id
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Los campos numéricos deben ser valores válidos"
            }), 400

        resultado = controlador_direcciones.agregar_direccion(
            usuario_id=datos['usuario_id'],
            direccion=datos['calle'] + ' ' + datos['numero'],
            ciudad_id=datos['ciudad_id'],
            estado_id=None,
            pais_id=None,
            codigo_postal=datos['codigo_postal'],
            distrito_id=datos['distrito_id']  # Agregado distrito_id
        )
        
        if resultado:
            return jsonify({
                "status": "success",
                "message": "Dirección creada exitosamente",
                "data": {"id": resultado}
            }), 201
        return jsonify({"status": "error", "message": "Error al crear la dirección"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/direcciones/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_direccion(id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "No se proporcionaron datos para actualizar"}), 400

        try:
            datos['ciudad_id'] = int(datos['ciudad_id'])
            datos['distrito_id'] = int(datos['distrito_id'])  # Agregado distrito_id
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Los campos numéricos deben ser valores válidos"
            }), 400

        resultado = controlador_direcciones.actualizar_direccion(id, datos)
        if resultado:
            return jsonify({"status": "success", "message": "Dirección actualizada exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al actualizar la dirección"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/direcciones/<int:id>/predeterminada', methods=['PUT'])
@jwt_required()
def api_establecer_direccion_predeterminada(id):
    try:
        direccion = controlador_direcciones.obtener_direccion_por_id(id)
        if not direccion:
            return jsonify({"status": "error", "message": "Dirección no encontrada"}), 404

        resultado = controlador_direcciones.establecer_direccion_predeterminada(
            direccion['usuario_id'], id
        )
        if resultado:
            return jsonify({"status": "success", "message": "Dirección establecida como predeterminada"}), 200
        return jsonify({"status": "error", "message": "Error al establecer la dirección como predeterminada"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/direcciones/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_direccion(id):
    try:
        direccion = controlador_direcciones.obtener_direccion_por_id(id)
        if not direccion:
            return jsonify({"status": "error", "message": "Dirección no encontrada"}), 404

        resultado = controlador_direcciones.eliminar_direccion(direccion['usuario_id'], id)
        if resultado:
            return jsonify({"status": "success", "message": "Dirección eliminada exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al eliminar la dirección"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Usuario
@app.route('/api/usuarios', methods=['GET'])
@jwt_required()
def api_obtener_usuarios():
    try:
        usuarios = controlador_usuario.obtener_todos_usuarios()
        return jsonify([{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'email': u.email,
            'tipo': u.tipo,
            'fecha_registro': u.fecha_registro
        } for u in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_usuario(id):
    try:
        usuario = controlador_usuario.obtener_usuario_por_id(id)
        if usuario:
            return jsonify({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'tipo': usuario.tipo,
                'fecha_registro': usuario.fecha_registro
            }), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios', methods=['POST'])
@jwt_required()
def api_crear_usuario():
    try:
        data = request.get_json()
        nuevo_usuario = controlador_usuario.crear_usuario(
            data['nombre'],
            data['apellido'],
            data['email'],
            data['contrasena'],
            data.get('tipo', 'cliente')
        )
        return jsonify({
            'mensaje': 'Usuario creado exitosamente',
            'id': nuevo_usuario.id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_usuario(id):
    try:
        data = request.get_json()
        usuario = controlador_usuario.actualizar_usuario(
            id,
            data.get('nombre'),
            data.get('apellido'),
            data.get('email'),
            data.get('tipo')
        )
        return jsonify({'mensaje': 'Usuario actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_usuario(id):
    try:
        controlador_usuario.eliminar_usuario(id)
        return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# APIs para Pedido
@app.route('/api/pedidos', methods=['GET'])
@jwt_required()
def api_obtener_pedidos():
    try:
        pedidos = controlador_pedido.obtener_pedidos()
        return jsonify({"status": "success", "data": pedidos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pedidos/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_pedido(id):
    try:
        pedido = controlador_pedido.obtener_pedido_por_id(id)
        if not pedido:
            return jsonify({"status": "error", "message": "Pedido no encontrado"}), 404
        return jsonify({"status": "success", "data": pedido}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pedidos', methods=['POST'])
@jwt_required()
def api_crear_pedido():
    try:
        datos = request.get_json()
        required_fields = ['usuario_id', 'productos', 'direccion_id']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400
        
        resultado = controlador_pedido.crear_pedido(
            datos['usuario_id'],
            datos['productos'],
            datos['direccion_id'],
            datos.get('metodo_pago_id'),
            datos.get('estado', 'pendiente')
        )
        if resultado:
            return jsonify({"status": "success", "message": "Pedido creado exitosamente", "data": resultado}), 201
        return jsonify({"status": "error", "message": "Error al crear el pedido"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pedidos/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_pedido(id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "Datos incompletos"}), 400

        pedido_actual = controlador_pedido.obtener_pedido_por_id(id)
        if not pedido_actual:
            return jsonify({"status": "error", "message": "Pedido no encontrado"}), 404

        resultado = controlador_pedido.actualizar_pedido(
            id,
            datos.get('estado', pedido_actual.estado),
            datos.get('direccion_id', pedido_actual.direccion_id),
            datos.get('metodo_pago_id', pedido_actual.metodo_pago_id)
        )
        if resultado:
            return jsonify({"status": "success", "message": "Pedido actualizado exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al actualizar el pedido"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pedidos/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_pedido(id):
    try:
        resultado = controlador_pedido.eliminar_pedido(id)
        if resultado:
            return jsonify({"status": "success", "message": "Pedido eliminado correctamente"}), 200
        return jsonify({"status": "error", "message": "Error al eliminar el pedido"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/pedidos/<int:id>/estado', methods=['PUT'])
@jwt_required()
def api_actualizar_estado_pedido(id):
    try:
        datos = request.get_json()
        if not datos or 'estado' not in datos:
            return jsonify({"status": "error", "message": "Estado no especificado"}), 400
        
        resultado = controlador_pedido.actualizar_estado_pedido(id, datos['estado'])
        if resultado:
            return jsonify({"status": "success", "message": "Estado del pedido actualizado exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al actualizar el estado del pedido"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Categorías
@app.route('/api/categorias', methods=['GET'])
@jwt_required()
def api_obtener_categorias():
    try:
        categorias = controlador_categorias.obtener_todas_categorias()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_categoria(id):
    try:
        categoria = controlador_categorias.obtener_categorias_por_id(id)
        if categoria:
            return jsonify(categoria), 200
        else:
            return jsonify({'error': 'Categoría no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias', methods=['POST'])
@jwt_required()
def api_crear_categoria():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
            
        resultado = controlador_categorias.insertar_categorias(data['nombre'])
        if resultado:
            return jsonify({'mensaje': 'Categoría creada exitosamente'}), 201
        else:
            return jsonify({'error': 'No se pudo crear la categoría'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_categoria(id):
    try:
        data = request.get_json()
        if not data or 'nombre' not in data:
            return jsonify({'error': 'El nombre de la categoría es requerido'}), 400
            
        controlador_categorias.actualizar_categorias(id, data['nombre'])
        return jsonify({'mensaje': 'Categoría actualizada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_categoria(id):
    try:
        controlador_categorias.eliminar_categorias(id)
        return jsonify({'mensaje': 'Categoría eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# APIs para Producto
@app.route('/api/productos', methods=['GET'])
@jwt_required()
def api_obtener_productos():
    try:
        categoria_id = request.args.get('categoria_id', type=int)
        
        if categoria_id:
            productos = controlador_producto.obtener_productos_por_categorias(categoria_id)
        else:
            productos = controlador_producto.obtener_todos_productos()
            
        # Convert products to dictionaries for JSON serialization
        productos_dict = [producto.to_dict() for producto in productos]
        return jsonify({"status": "success", "data": productos_dict}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_producto(id):
    try:
        producto = controlador_producto.obtener_producto_por_id(id)
        if not producto:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404
        return jsonify({"status": "success", "data": producto.to_dict()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos', methods=['POST'])
@jwt_required()
def api_crear_producto():
    try:
        datos = request.get_json()
        required_fields = ['nombre', 'descripcion', 'precio', 'categoria_id', 'stock']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        try:
            datos['precio'] = float(datos['precio'])
            datos['stock'] = int(datos['stock'])
            datos['categoria_id'] = int(datos['categoria_id'])
            if 'marca_id' in datos:
                datos['marca_id'] = int(datos['marca_id'])
            if 'modelo_id' in datos:
                datos['modelo_id'] = int(datos['modelo_id'])
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Los campos numéricos deben ser valores válidos"
            }), 400

        resultado = controlador_producto.crear_producto(datos)
        if resultado:
            return jsonify({
                "status": "success",
                "message": "Producto creado exitosamente",
                "data": {"id": resultado}
            }), 201
        return jsonify({"status": "error", "message": "Error al crear el producto"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_producto(id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "No se proporcionaron datos para actualizar"}), 400

        producto_existente = controlador_producto.obtener_producto_por_id(id)
        if not producto_existente:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        try:
            if 'precio' in datos:
                datos['precio'] = float(datos['precio'])
            if 'stock' in datos:
                datos['stock'] = int(datos['stock'])
            if 'categoria_id' in datos:
                datos['categoria_id'] = int(datos['categoria_id'])
            if 'marca_id' in datos:
                datos['marca_id'] = int(datos['marca_id'])
            if 'modelo_id' in datos:
                datos['modelo_id'] = int(datos['modelo_id'])
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Los campos numéricos deben ser valores válidos"
            }), 400

        resultado = controlador_producto.actualizar_producto(id, datos)
        if resultado:
            return jsonify({"status": "success", "message": "Producto actualizado exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al actualizar el producto"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_producto(id):
    try:
        producto = controlador_producto.obtener_producto_por_id(id)
        if not producto:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        resultado = controlador_producto.eliminar_producto(id)
        if resultado:
            return jsonify({"status": "success", "message": "Producto eliminado exitosamente"}), 200
        return jsonify({"status": "error", "message": "Error al eliminar el producto"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/buscar', methods=['GET'])
@jwt_required()
def api_buscar_productos():
    try:
        query = request.args.get('q', '')
        categoria_id = request.args.get('categoria_id', type=int)
        precio_min = request.args.get('precio_min', type=float)
        precio_max = request.args.get('precio_max', type=float)
        marca_id = request.args.get('marca_id', type=int)
        modelo_id = request.args.get('modelo_id', type=int)

        productos = controlador_producto.busqueda_avanzada(
            query=query,
            categoria_id=categoria_id,
            precio_min=precio_min,
            precio_max=precio_max,
            id_marca=marca_id,
            id_modelo=modelo_id
        )
        return jsonify({"status": "success", "data": [p.to_dict() for p in productos]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/destacados', methods=['GET'])
@jwt_required()
def api_obtener_productos_destacados():
    try:
        limite = request.args.get('limite', 4, type=int)
        productos = controlador_producto.obtener_productos_destacados(limite)
        return jsonify({"status": "success", "data": [p.to_dict() for p in productos]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/productos/<int:id>/relacionados', methods=['GET'])
@jwt_required()
def api_obtener_productos_relacionados(id):
    try:
        limite = request.args.get('limite', 4, type=int)
        productos = controlador_producto.obtener_productos_relacionados(id, limite)
        return jsonify({"status": "success", "data": [p.to_dict() for p in productos]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs de Favoritos
@app.route('/api/usuarios/<int:usuario_id>/favoritos', methods=['GET'])
@jwt_required()
def api_obtener_favoritos_usuario(usuario_id):
    try:
        favoritos = controlador_favorito.obtener_favoritos_usuario(usuario_id)
        return jsonify({"status": "success", "data": favoritos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/favoritos/<int:producto_id>', methods=['POST'])
@jwt_required()
def api_agregar_favorito(usuario_id, producto_id):
    try:
        producto = controlador_producto.obtener_producto_por_id(producto_id)
        if not producto:
            return jsonify({"status": "error", "message": "Producto no encontrado"}), 404

        resultado = controlador_favorito.agregar_favorito(usuario_id, producto_id)
        if resultado:
            return jsonify({"status": "success", "message": "Producto agregado a favoritos"}), 201
        return jsonify({"status": "error", "message": "Error al agregar el producto a favoritos"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/favoritos/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_favorito(usuario_id, producto_id):
    try:
        resultado = controlador_favorito.eliminar_favorito(usuario_id, producto_id)
        if resultado:
            return jsonify({"status": "success", "message": "Producto eliminado de favoritos"}), 200
        return jsonify({"status": "error", "message": "Producto no encontrado en favoritos"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/favoritos/verificar/<int:producto_id>', methods=['GET'])
@jwt_required()
def api_verificar_favorito(usuario_id, producto_id):
    try:
        es_favorito = controlador_favorito.existe_favorito(usuario_id, producto_id)
        return jsonify({
            "status": "success", 
            "data": {"es_favorito": es_favorito}
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/usuarios/<int:usuario_id>/favoritos/toggle/<int:producto_id>', methods=['POST'])
@jwt_required()
def api_toggle_favorito(usuario_id, producto_id):
    try:
        # Verificar si ya existe como favorito
        es_favorito = controlador_favorito.existe_favorito(usuario_id, producto_id)
        
        if es_favorito:
            # Si existe, lo eliminamos
            controlador_favorito.eliminar_favorito(usuario_id, producto_id)
            mensaje = "Producto eliminado de favoritos"
        else:
            # Si no existe, lo agregamos
            controlador_favorito.agregar_favorito(usuario_id, producto_id)
            mensaje = "Producto agregado a favoritos"
            
        return jsonify({
            "status": "success",
            "message": mensaje,
            "data": {"es_favorito": not es_favorito}
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Kit
@app.route('/api/kits/<int:usuario_id>', methods=['GET'])
@jwt_required()
def api_obtener_kits_usuario(usuario_id):
    try:
        kits = controlador_kit.obtener_kits_usuario(usuario_id)
        return jsonify({"status": "success", "data": kits}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/kits/<int:kit_id>', methods=['GET'])
@jwt_required()
def api_obtener_kit(kit_id):
    try:
        kit = controlador_kit.obtener_kit_por_id(kit_id)
        if not kit:
            return jsonify({"status": "error", "message": "Kit no encontrado"}), 404
        return jsonify({"status": "success", "data": kit}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/kits', methods=['POST'])
@jwt_required()
def api_crear_kit():
    try:
        datos = request.get_json()
        required_fields = ['usuario_id', 'celular_id', 'smartwatch_id', 'accesorios_id']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        controlador_kit.crear_kit(
            datos['usuario_id'],
            datos['celular_id'],
            datos['smartwatch_id'],
            datos['accesorios_id']
        )
        return jsonify({"status": "success", "message": "Kit creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/kits/<int:kit_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_kit(kit_id):
    try:
        controlador_kit.eliminar_kit(kit_id)
        return jsonify({"status": "success", "message": "Kit eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/kits/usuario/<int:usuario_id>/recientes', methods=['GET'])
@jwt_required()
def api_obtener_kits_recientes(usuario_id):
    try:
        kits = controlador_kit.obtener_kits_usuario(usuario_id)
        # Limitamos a los 5 más recientes
        kits_recientes = kits[:5] if len(kits) > 5 else kits
        return jsonify({"status": "success", "data": kits_recientes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Opiniones
@app.route('/api/opiniones/producto/<int:producto_id>', methods=['GET'])
@jwt_required()
def api_obtener_opiniones_producto(producto_id):
    try:
        opiniones = controlador_opinion.obtener_opiniones_producto(producto_id)
        return jsonify({"status": "success", "data": opiniones}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/opiniones', methods=['POST'])
@jwt_required()
def api_agregar_opinion():
    try:
        datos = request.get_json()
        required_fields = ['producto_id', 'usuario_id', 'comentario', 'calificacion']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        controlador_opinion.agregar_opiniones(
            datos['producto_id'],
            datos['usuario_id'],
            datos['comentario'],
            datos['calificacion']
        )
        return jsonify({"status": "success", "message": "Opinión agregada exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/opiniones/producto/<int:producto_id>/promedio', methods=['GET'])
@jwt_required()
def api_obtener_calificacion_promedio(producto_id):
    try:
        promedio = controlador_opinion.calcular_calificacion_promedio(producto_id)
        return jsonify({"status": "success", "data": {"promedio": promedio}}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/opiniones/recientes', methods=['GET'])
@jwt_required()
def api_obtener_opiniones_recientes():
    try:
        limite = request.args.get('limite', 5, type=int)
        opiniones = controlador_opinion.obtener_opiniones_producto(None)  # Modificar el controlador para aceptar límite
        opiniones_recientes = opiniones[:limite]
        return jsonify({"status": "success", "data": opiniones_recientes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/opiniones/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def api_obtener_opiniones_usuario(usuario_id):
    try:
        opiniones = controlador_opinion.obtener_opiniones_producto(None)  # Modificar el controlador para filtrar por usuario
        return jsonify({"status": "success", "data": opiniones}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Notificaciones
@app.route('/api/notificaciones/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def api_obtener_notificaciones_usuario(usuario_id):
    try:
        notificaciones = controlador_notificaciones.obtener_notificaciones()
        return jsonify({"status": "success", "data": notificaciones}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/notificaciones', methods=['POST'])
@jwt_required()
def api_crear_notificacion():
    try:
        datos = request.get_json()
        required_fields = ['usuario_id', 'pedido_id', 'mensaje']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        controlador_notificaciones.agregar_notificacion(
            datos['usuario_id'],
            datos['pedido_id'],
            datos['mensaje']
        )
        return jsonify({"status": "success", "message": "Notificación creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/notificaciones/<int:notificacion_id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_notificacion(notificacion_id):
    try:
        controlador_notificaciones.eliminar_notificacion(notificacion_id)
        return jsonify({"status": "success", "message": "Notificación eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/notificaciones/<int:notificacion_id>/marcar-vista', methods=['PUT'])
@jwt_required()
def api_marcar_notificacion_vista(notificacion_id):
    try:
        controlador_notificaciones.marcar_notificacion_como_vista(notificacion_id)
        return jsonify({"status": "success", "message": "Notificación marcada como vista"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/notificaciones/recientes', methods=['GET'])
@jwt_required()
def api_obtener_notificaciones_recientes():
    try:
        notificaciones = controlador_notificaciones.obtener_notificaciones_recientes()
        return jsonify({"status": "success", "data": notificaciones}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Método de Pago
@app.route('/api/metodos-pago/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def api_listar_metodos_pago(usuario_id):
    try:
        metodos = controlador_metodo_pago.listar_metodos_pago(usuario_id)
        return jsonify({"status": "success", "data": metodos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/metodos-pago/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_metodo_pago(id):
    try:
        metodo = controlador_metodo_pago.obtener_metodo_pago(id)
        if not metodo:
            return jsonify({"status": "error", "message": "Método de pago no encontrado"}), 404
        return jsonify({"status": "success", "data": metodo}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/metodos-pago', methods=['POST'])
@jwt_required()
def api_insertar_metodo_pago():
    try:
        datos = request.get_json()
        required_fields = ['usuario_id', 'tipo', 'numero_tarjeta', 'titular', 'fecha_vencimiento', 'cvv']
        if not datos or not all(field in datos for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"Datos incompletos. Se requieren los campos: {', '.join(required_fields)}"
            }), 400

        metodo = MetodoPago(
            id=None,
            usuario_id=datos['usuario_id'],
            tipo=datos['tipo'],
            numero_tarjeta=datos['numero_tarjeta'],
            titular=datos['titular'],
            fecha_vencimiento=datos['fecha_vencimiento'],
            cvv=datos['cvv'],
            predeterminado=datos.get('predeterminado', False),
            fecha_registro=datetime.now(),
            activo=True
        )
        
        controlador_metodo_pago.insertar_metodo_pago(metodo)
        return jsonify({"status": "success", "message": "Método de pago agregado exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/metodos-pago/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_metodo_pago(id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"status": "error", "message": "No se proporcionaron datos para actualizar"}), 400

        controlador_metodo_pago.actualizar_metodo_pago(id, datos)
        return jsonify({"status": "success", "message": "Método de pago actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/metodos-pago/<int:id>/predeterminado', methods=['PUT'])
@jwt_required()
def api_establecer_metodo_pago_predeterminado(id):
    try:
        datos = request.get_json()
        if 'usuario_id' not in datos:
            return jsonify({"status": "error", "message": "Se requiere el ID del usuario"}), 400

        controlador_metodo_pago.establecer_predeterminado(id, datos['usuario_id'])
        return jsonify({"status": "success", "message": "Método de pago establecido como predeterminado"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Marca
@app.route('/api/marcas', methods=['GET'])
@jwt_required()
def api_obtener_marcas():
    try:
        marcas = controlador_marca.obtener_marcas()
        return jsonify({"status": "success", "data": marcas}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marcas/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_marca(id):
    try:
        marca = controlador_marca.obtener_marca_por_id(id)
        if not marca:
            return jsonify({"status": "error", "message": "Marca no encontrada"}), 404
        return jsonify({"status": "success", "data": marca}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marcas', methods=['POST'])
@jwt_required()
def api_crear_marca():
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos:
            return jsonify({"status": "error", "message": "Se requiere el nombre de la marca"}), 400

        marca = Marca(nombre=datos['nombre'])
        controlador_marca.insertar_marca(marca)
        return jsonify({"status": "success", "message": "Marca creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marcas/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_marca(id):
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos:
            return jsonify({"status": "error", "message": "Se requiere el nombre de la marca"}), 400

        controlador_marca.actualizar_marca(id, datos['nombre'])
        return jsonify({"status": "success", "message": "Marca actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/marcas/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_marca(id):
    try:
        controlador_marca.eliminar_marca(id)
        return jsonify({"status": "success", "message": "Marca eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs para Modelo
@app.route('/api/modelos', methods=['GET'])
@jwt_required()
def api_obtener_modelos():
    try:
        modelos = controlador_modelo.obtener_modelos()
        return jsonify({"status": "success", "data": modelos}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/modelos/<int:id>', methods=['GET'])
@jwt_required()
def api_obtener_modelo(id):
    try:
        modelo = controlador_modelo.obtener_modelo_por_id(id)
        if not modelo:
            return jsonify({"status": "error", "message": "Modelo no encontrado"}), 404
        return jsonify({"status": "success", "data": modelo}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/modelos', methods=['POST'])
@jwt_required()
def api_crear_modelo():
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos:
            return jsonify({"status": "error", "message": "Se requiere el nombre del modelo"}), 400

        modelo = Modelo(nombre=datos['nombre'])
        controlador_modelo.insertar_modelo(modelo)
        return jsonify({"status": "success", "message": "Modelo creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/modelos/<int:id>', methods=['PUT'])
@jwt_required()
def api_actualizar_modelo(id):
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos:
            return jsonify({"status": "error", "message": "Se requiere el nombre del modelo"}), 400

        modelo = Modelo(nombre=datos['nombre'], id=id)
        controlador_modelo.actualizar_modelo(modelo)
        return jsonify({"status": "success", "message": "Modelo actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/modelos/<int:id>', methods=['DELETE'])
@jwt_required()
def api_eliminar_modelo(id):
    try:
        controlador_modelo.eliminar_modelo(id)
        return jsonify({"status": "success", "message": "Modelo eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# APIs de Chatbot
@app.route('/api/chatbot/consulta', methods=['POST'])
@jwt_required()
def api_chatbot_consulta():
    try:
        data = request.get_json()
        respuesta = {
            'mensaje': 'Lo siento, el chatbot está en mantenimiento.',
            'sugerencias': [
                'Revisa nuestras preguntas frecuentes',
                'Contacta a servicio al cliente',
                'Explora nuestro catálogo'
            ]
        }
        return jsonify(respuesta), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/feedback', methods=['POST'])
@jwt_required()
def api_chatbot_feedback():
    try:
        data = request.get_json()
        return jsonify({'mensaje': 'Gracias por tu feedback'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# APIs de Reportes
@app.route('/api/reportes/ventas/diarias', methods=['GET'])
@jwt_required()
def api_reporte_ventas_diarias():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        from controlador_pedido import ControladorPedido
        reporte = ControladorPedido.generar_reporte_ventas_diarias(fecha_inicio, fecha_fin)
        return jsonify(reporte), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reportes/productos/stock-bajo', methods=['GET'])
@jwt_required()
def api_reporte_productos_stock_bajo():
    try:
        limite = request.args.get('limite', 10)
        from controlador_producto import ControladorProducto
        productos = ControladorProducto.obtener_productos_stock_bajo(limite)
        return jsonify([{
            'id': p.id,
            'nombre': p.nombre,
            'stock_actual': p.stock,
            'stock_minimo': p.stock_minimo
        } for p in productos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reportes/usuarios/actividad', methods=['GET'])
@jwt_required()
def api_reporte_actividad_usuarios():
    try:
        periodo = request.args.get('periodo', '7d')
        from controlador_usuario import ControladorUsuario
        reporte = ControladorUsuario.generar_reporte_actividad(periodo)
        return jsonify(reporte), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# APIs de Exportación
@app.route('/api/exportar/productos', methods=['GET'])
@jwt_required()
def api_exportar_productos():
    try:
        formato = request.args.get('formato', 'csv')
        from controlador_producto import ControladorProducto
        datos = ControladorProducto.exportar_productos(formato)
        return jsonify({
            'datos': datos,
            'formato': formato
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exportar/pedidos', methods=['GET'])
@jwt_required()
def api_exportar_pedidos():
    try:
        formato = request.args.get('formato', 'csv')
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        from controlador_pedido import ControladorPedido
        datos = ControladorPedido.exportar_pedidos(formato, fecha_inicio, fecha_fin)
        return jsonify({
            'datos': datos,
            'formato': formato
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)