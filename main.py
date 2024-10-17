from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, request, make_response
from functools import wraps
from werkzeug.utils import secure_filename
import os
from bd import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash
import controlador_usuario
import controlador_categorias
import controlador_producto
import controlador_pedido
import controlador_kit
import controlador_favorito
import controlador_direcciones
import controlador_opinion

#PROYECTO ACTUALIZADO 10/11/2024

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
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
        contraseña = request.form['contraseña']
        
        usuario = controlador_usuario.obtener_usuario_por_email(email)
        
        if usuario and controlador_usuario.check_password(usuario.contraseña, contraseña):
            session['usuario_id'] = usuario.id
            session['usuario_tipo'] = usuario.tipo
            session['usuario_nombre'] = usuario.nombre.split()[0] if usuario.nombre else ""
            session['usuario_apellido'] = usuario.apellido.split()[0] if usuario.apellido else ""
            flash('Inicio de sesión exitoso', 'success')
            
            if usuario.tipo == 'administrador':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Credenciales inválidas', 'error')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        if controlador_usuario.insertar_usuario(nombre, apellido, email, contraseña, 'cliente', None):
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error en el registro. Por favor, intenta de nuevo.', 'error')

    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home'))

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
        print(f"Error al agregar favorito: {e}")  # Ver más detalles en consola
        return jsonify(success=False, message="Error interno, inténtalo nuevamente")

@app.route('/eliminar-favorito/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_favorito(producto_id):
    usuario_id = session.get('usuario_id')
    try:
        controlador_favorito.eliminar_favorito(usuario_id, producto_id)
        return render_template('mis_favoritos.html')
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
        usuario_id = session['usuario_id']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        pais = request.form['pais']
        codigo_postal = request.form['codigo_postal']
        
        controlador_direcciones.agregar_direccion(usuario_id, direccion, ciudad, estado, pais, codigo_postal)
        flash('Dirección agregada con éxito', 'success')
        return redirect(url_for('mis_direcciones'))
    
    return render_template('agregar_direccion.html')

@app.route('/editar-direccion/<int:direccion_id>', methods=['GET', 'POST'])
@login_required
def editar_direccion(direccion_id):
    direccion = controlador_direcciones.obtener_direccion_por_id(direccion_id)
    
    if request.method == 'POST':
        nueva_direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        estado = request.form['estado']
        pais = request.form['pais']
        codigo_postal = request.form['codigo_postal']

        controlador_direcciones.actualizar_direccion(direccion_id, nueva_direccion, ciudad, estado, pais, codigo_postal)
        flash('Dirección actualizada con éxito', 'success')
        return redirect(url_for('mis_direcciones'))

    return render_template('editar_direccion.html', direccion=direccion)

@app.route('/mis-direcciones')
@login_required
def mis_direcciones():
    direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
    return render_template('mis_direcciones.html', direcciones=direcciones)

@app.route('/producto/<int:id>')
def producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    opiniones = controlador_producto.obtener_opiniones(id)
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
    query = request.args.get('q', '').strip()  # Capturamos el término de búsqueda y eliminamos espacios
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

    # Verificar si el producto ya está en el carrito
    for item in session['carrito']:
        if item['producto_id'] == producto_id:
            item['cantidad'] += cantidad
            session.modified = True
            flash('Producto actualizado en el carrito', 'success')
            return redirect(url_for('carrito'))

    # Si no está en el carrito, agregarlo
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

@app.route('/eliminar-del-carrito/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(producto_id):
    if 'carrito' in session:
        session['carrito'] = [item for item in session['carrito'] if item['producto_id'] != producto_id]
        session.modified = True
        flash('Producto eliminado del carrito', 'success')
    return redirect(url_for('carrito'))

@app.route('/actualizar-carrito', methods=['POST'])
@login_required
def actualizar_carrito():
    if 'carrito' in session:
        for item in session['carrito']:
            cantidad = int(request.form.get(f'cantidad_{item["producto_id"]}', 0))
            if cantidad > 0:
                item['cantidad'] = cantidad
            else:
                session['carrito'].remove(item)
        session.modified = True
        flash('Carrito actualizado', 'success')
    return redirect(url_for('carrito'))

@app.route('/realizar-pedido', methods=['GET', 'POST'])
@login_required
def realizar_pedido():
    if 'carrito' not in session or not session['carrito']:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('carrito'))

    if request.method == 'POST':
        direccion_id = request.form.get('direccion_id')
        if not direccion_id:
            flash('Debes seleccionar una dirección de envío', 'error')
            return redirect(url_for('realizar_pedido'))

        try:
            pedido_id = controlador_pedido.crear_pedido(session['usuario_id'], int(direccion_id))
            
            for item in session['carrito']:
                controlador_pedido.agregar_detalle_pedido(pedido_id, item['producto_id'], int(item['cantidad']), float(item['precio']))
                try:
                    controlador_producto.actualizar_stock(item['producto_id'], -int(item['cantidad']))
                except ValueError as e:
                    controlador_pedido.eliminar_pedido(pedido_id)
                    flash(str(e), 'error')
                    return redirect(url_for('carrito'))

            session.pop('carrito', None)
            flash('Pedido realizado con éxito', 'success')
            return redirect(url_for('confirmacion_pedido', pedido_id=pedido_id))
        except Exception as e:
            flash(f'Error al crear el pedido: {str(e)}', 'error')
            return redirect(url_for('realizar_pedido'))

    direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
    total = sum(int(item['cantidad']) * float(item['precio']) for item in session['carrito'])
    return render_template('realizar_pedido.html', direcciones=direcciones, total=total)

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

@app.route('/admin')
@admin_required
def admin_dashboard():
    total_productos = controlador_producto.contar_productos()
    pedidos_pendientes = controlador_pedido.contar_pedidos_pendientes()
    total_usuarios = controlador_usuario.contar_usuarios()
    ingresos_mes = controlador_pedido.calcular_ingresos_mes()
    return render_template('admin/dashboard.html', 
                           total_productos=total_productos,
                           pedidos_pendientes=pedidos_pendientes,
                           total_usuarios=total_usuarios,
                           ingresos_mes=ingresos_mes)

@app.route('/admin/productos')
@admin_required
def admin_productos():
    productos = controlador_producto.obtener_todos_productos()
    return render_template('admin/productos.html', productos=productos)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/nuevo_producto', methods=['GET', 'POST'])
def admin_nuevo_producto():
    categorias = controlador_categorias.obtener_todas_categorias()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        destacado = 1 if 'destacado' in request.form else 0

        imagen = request.files['imagen']
        imagen_filename = None
        if imagen and allowed_file(imagen.filename):
            try:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            except Exception as e:
                flash(f'Error al cargar la imagen: {str(e)}', 'error')
                return redirect(url_for('admin_nuevo_producto'))

        try:
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
        except Exception as e:
            flash(f'Error al crear el producto: {str(e)}', 'error')

        return redirect(url_for('admin_productos'))

    return render_template('admin/editar_nuevo_producto.html', producto=None, categorias=categorias)

@app.route('/admin/editar_producto/<int:id>', methods=['GET', 'POST'])
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
                return redirect(url_for('admin_productos', id=id))

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

        return redirect(url_for('admin_editar_producto', id=id))

    return render_template('admin/editar_nuevo_producto.html', producto=producto, categorias=categorias)

@app.route('/admin/producto/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_producto(id):
    controlador_producto.eliminar_producto(id)
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('admin_productos'))

@app.route('/admin/pedidos')
@login_required
def admin_pedidos():
    pedidos = controlador_pedido.obtener_todos_pedidos()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@app.route('/admin/pedido/<int:id>', methods=['GET'])
@admin_required
def admin_detalle_pedido(id):
    pedido = controlador_pedido.obtener_pedido_por_id(id)
    if not pedido:
        flash('Pedido no encontrado', 'error')
        return redirect(url_for('admin_pedidos'))
    return render_template('admin/detalle_pedido.html', pedido=pedido)

@app.route('/admin/pedido/actualizar-estado/<int:id>', methods=['POST'])
@admin_required
def admin_actualizar_estado_pedido(id):
    nuevo_estado = request.form.get('nuevo_estado')
    controlador_pedido.actualizar_estado_pedido(id, nuevo_estado)
    flash('Estado del pedido actualizado con éxito', 'success')
    return redirect(url_for('admin_pedidos', id=id))

@app.route('/admin/pedido/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_pedido(id):
    pedido = controlador_pedido.obtener_pedido_por_id(id)
    
    if request.method == 'POST':
        # Recogemos los datos de la dirección del formulario
        calle = request.form.get('calle')
        ciudad = request.form.get('ciudad')
        estado = request.form.get('estado')
        pais = request.form.get('pais')
        fecha_pedido = request.form.get('fecha_pedido')
        estado_pedido = request.form.get('estado')

        if calle and ciudad and estado and pais and fecha_pedido and estado_pedido:
            try:
                controlador_pedido.editar_pedido(id, calle, ciudad, estado, pais, fecha_pedido, estado_pedido)
                flash('Pedido actualizado con éxito', 'success')
                return redirect(url_for('admin_pedidos', id=id))
            except Exception as e:
                flash(f'Error al actualizar el pedido: {str(e)}', 'error')
        else:
            flash('Faltan campos por completar', 'error')
    
    return render_template('admin/editar_pedido.html', pedido=pedido)


@app.route('/admin/pedido/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_pedido(id):
    controlador_pedido.eliminar_pedido(id)
    flash('Pedido eliminado con éxito', 'success')
    return redirect(url_for('admin_pedidos'))   

@app.route('/admin/categorias')
@admin_required
def admin_categorias():
    categorias = controlador_categorias.obtener_todas_categorias()
    return render_template('admin/categorias.html', categorias=categorias)

@app.route('/admin/categorias/nueva', methods=['GET', 'POST'])
@admin_required
def admin_nueva_categorias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        controlador_categorias.insertar_categorias(nombre)
        flash('Categoría creada con éxito', 'success')
        return redirect(url_for('admin_categorias'))
    return render_template('admin/nueva_categoria.html')

@app.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_categorias(id):
    categorias = controlador_categorias.obtener_categorias_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        controlador_categorias.actualizar_categorias(id, nombre)
        flash('Categoría actualizada con éxito', 'success')
        return redirect(url_for('admin_categorias'))
    return render_template('admin/editar_categorias.html', categorias=categorias)

@app.route('/admin/categorias/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_categorias(id):
    controlador_categorias.eliminar_categorias(id)
    flash('Categoría eliminada con éxito', 'success')
    return redirect(url_for('admin_categorias'))

@app.route('/admin/usuarios')
@admin_required
def admin_usuarios():
    usuarios = controlador_usuario.obtener_todos_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/admin/usuario/<int:id>/detalle', methods=['GET'])
@admin_required
def admin_detalle_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template('admin/detalle_usuario.html', usuario=usuario)

@app.route('/admin/usuario/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        tipo = request.form['tipo']
        nueva_contraseña = request.form.get('contraseña')  # La nueva contraseña es opcional
        
        foto = request.files.get('foto')  # Obtiene el archivo de imagen desde el formulario
        if foto and allowed_file(foto.filename):
            try:
                filename = secure_filename(foto.filename)  # Nombre seguro para el archivo
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto.save(foto_path)  # Guarda la imagen en la carpeta de subida
            except Exception as e:
                flash('Error al subir la imagen: ' + str(e), 'error')
                return redirect(url_for('editar_usuario', id=id))
        else:
            filename = usuario.foto  # Mantiene la foto actual si no se sube una nueva

        controlador_usuario.actualizar_usuario(
            id=id,
            nombre=nombre,
            apellido=apellido,
            email=email,
            tipo=tipo,
            foto=filename,
            nueva_contraseña=nueva_contraseña if nueva_contraseña else None
        )

        flash('Usuario actualizado con éxito', 'success')
        return redirect(url_for('admin_usuarios'))

    return render_template('admin/editar_usuario.html', usuario=usuario)


@app.route('/admin/usuario/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_usuario(id):
    try:
        controlador_usuario.eliminar_usuario(id)
        flash('Usuario eliminado con éxito', 'success')
    except Exception as e:
        flash(f'Error al eliminar el usuario: {str(e)}', 'error')
    return redirect(url_for('admin_usuarios'))


@app.route('/producto/<int:id>/opiniones', methods=['POST'])
@login_required
def agregar_opiniones(id):
    calificacion = int(request.form.get('calificacion'))
    comentario = request.form.get('comentario')
    usuario_id = session['usuario_id']

    controlador_producto.agregar_opiniones(id, usuario_id, calificacion, comentario)
    flash('Reseña agregada con éxito', 'success')
    return redirect(url_for('producto', id=id))

@app.route('/mi-cuenta')
@login_required
def mi_cuenta():
    usuario_id = session.get('usuario_id')
    usuario = controlador_usuario.obtener_usuario_por_id(usuario_id)
    return render_template('mi_cuenta.html', usuario=usuario)

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

@app.route('/cambiar-contraseña', methods=['GET', 'POST'])
@login_required
def cambiar_contraseña():
    if request.method == 'POST':
        contraseña_actual = request.form['contraseña_actual']
        nueva_contraseña = request.form['nueva_contraseña']
        confirmar_contraseña = request.form['confirmar_contraseña']
        
        usuario = controlador_usuario.obtener_usuario_por_id(session['usuario_id'])
        if check_password_hash(usuario.contraseña, contraseña_actual):
            if nueva_contraseña == confirmar_contraseña:
                hashed_password = generate_password_hash(nueva_contraseña)
                controlador_usuario.actualizar_contraseña(session['usuario_id'], hashed_password)
                flash('Contraseña actualizada correctamente', 'success')
                return redirect(url_for('mi_cuenta'))
            else:
                flash('Las contraseñas nuevas no coinciden', 'error')
        else:
            flash('La contraseña actual es incorrecta', 'error')
    
    return render_template('cambiar_contraseña.html')

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
