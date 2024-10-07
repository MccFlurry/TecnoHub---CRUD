from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion
import controlador_usuario
import controlador_categorias
import controlador_producto
import controlador_pedido
import controlador_kit
import controlador_favorito
import controlador_direcciones
import controlador_producto_visitado
import controlador_opinion

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta real
UPLOAD_FOLDER = 'static/img'  # Directorio donde se guardarán las imágenes
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
    return render_template('home.html', productos=productos_destacados, categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        usuario = controlador_usuario.obtener_usuario_por_email(email)
        if usuario and check_password_hash(usuario.contraseña, contrasena):
            session['usuario_id'] = usuario.id
            session['usuario_tipo'] = usuario.tipo

            primer_nombre = usuario.nombre.split()[0] if usuario.nombre else ""
            primer_apellido = usuario.apellido.split()[0] if usuario.apellido else ""
            
            session['usuario_nombre'] = primer_nombre
            session['usuario_apellido'] = primer_apellido
            
            flash('Inicio de sesión exitoso', 'success')
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
        contrasena = generate_password_hash(request.form['contrasena'])
        controlador_usuario.insertar_usuario(nombre, apellido, email, contrasena, 'cliente', None)
        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_tipo', None)
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home'))

@app.route('/categorias/<int:id>')
def categorias(id):
    categorias = controlador_categorias.obtener_categorias_por_id(id)
    if not categorias:
        flash('Categoría no encontrada', 'error')
        return redirect(url_for('home'))

    productos = controlador_producto.obtener_productos_por_categorias(id)

    return render_template('categorias.html', categorias=categorias, productos=productos)

@app.route('/categorias')
def todas_categorias():
    categorias = controlador_categorias.obtener_todas_categorias()
    return render_template('categorias.html', categorias=categorias)


@app.route('/arma-tu-kit', methods=['GET', 'POST'])
def arma_tu_kit():
    if request.method == 'POST':
        celular_id = request.form.get('celular_id')
        funda_id = request.form.get('funda_id')
        audifonos_id = request.form.get('audifonos_id')
        usuario_id = session.get('usuario_id')

        if usuario_id:
            controlador_kit.crear_kit(usuario_id, celular_id, funda_id, audifonos_id)
            flash('Kit creado con éxito', 'success')
            return redirect(url_for('mis_kits'))
        else:
            flash('Debes iniciar sesión para crear un kit', 'error')
            return redirect(url_for('login'))

    celulares = controlador_producto.obtener_productos_por_categorias(1)  # Asumiendo que 1 es la categoría de celulares
    fundas = controlador_producto.obtener_productos_por_categorias(2)     # Asumiendo que 2 es la categoría de fundas
    audifonos = controlador_producto.obtener_productos_por_categorias(3)  # Asumiendo que 3 es la categoría de audífonos

    return render_template('arma_tu_kit.html', celulares=celulares, fundas=fundas, audifonos=audifonos)

@app.route('/agregar-favorito/<int:producto_id>', methods=['POST'])
@login_required
def agregar_favorito(producto_id):
    usuario_id = session.get('usuario_id')
    controlador_favorito.agregar_favorito(usuario_id, producto_id)
    flash('Producto agregado a favoritos', 'success')
    return redirect(url_for('producto', id=producto_id))

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
        direccion = request.form.get('direccion')
        ciudad = request.form.get('ciudad')
        estado = request.form.get('estado')
        pais = request.form.get('pais')
        codigo_postal = request.form.get('codigo_postal')

        controlador_direcciones.agregar_direccion(session['usuario_id'], direccion, ciudad, estado, pais, codigo_postal)
        flash('Dirección agregada con éxito', 'success')
        return redirect(url_for('mis_direcciones'))
    
    return render_template('agregar_direccion.html')

@app.route('/mis-direcciones')
@login_required
def mis_direcciones():
    direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
    return render_template('mis_direcciones.html', direcciones=direcciones)

@app.route('/producto/<int:id>')
def producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    opiniones = controlador_producto.obtener_opinioness(id)
    productos_relacionados = controlador_producto.obtener_productos_relacionados(id)
    promedio_calificacion = controlador_opinion.calcular_calificacion_promedio(id)
    return render_template(
        'producto.html', 
        producto=producto, 
        opiniones=opiniones, 
        productos_relacionados=productos_relacionados,
        promedio_calificacion=promedio_calificacion 
    )

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    productos = controlador_producto.buscar_productos(query)
    return render_template('resultados_busqueda.html', productos=productos, query=query)

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
    total = sum(item['cantidad'] * item['precio'] for item in session.get('carrito', []))
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

        pedido_id = controlador_pedido.crear_pedido(session['usuario_id'], direccion_id)

        for item in session['carrito']:
            controlador_pedido.agregar_detalle_pedido(pedido_id, item['producto_id'], item['cantidad'], item['precio'])
            controlador_producto.actualizar_stock(item['producto_id'], -item['cantidad'])

        # Limpiar el carrito después de realizar el pedido
        session.pop('carrito', None)
        flash('Pedido realizado con éxito', 'success')
        return redirect(url_for('confirmacion_pedido', pedido_id=pedido_id))

    direcciones = controlador_direcciones.obtener_direcciones_usuario(session['usuario_id'])
    total = sum(item['cantidad'] * item['precio'] for item in session['carrito'])
    return render_template('realizar_pedido.html', direcciones=direcciones, total=total)

@app.route('/confirmacion-pedido/<int:pedido_id>')
@login_required
def confirmacion_pedido(pedido_id):
    pedido = controlador_pedido.obtener_pedido_por_id(pedido_id)
    if not pedido or pedido.usuario_id != session['usuario_id']:
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
@admin_required
def admin_nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categorias_id = request.form['categorias_id']
        precio = request.form['precio']
        stock = request.form['stock']
        destacado = 1 if 'destacado' in request.form else 0

        # Procesar la imagen
        imagen = request.files['imagen']
        imagen_filename = None
        
        if imagen and allowed_file(imagen.filename):
            try:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            except Exception as e:
                flash('Error al cargar la imagen: ' + str(e), 'error')
                return redirect(url_for('admin_nuevo_producto'))
        else:
            flash('El formato de la imagen no es válido. Debe ser .png, .jpg, .jpeg o .gif', 'error')
            return redirect(url_for('admin_nuevo_producto'))

        # Guarda el producto en la base de datos
        try:
            controlador_producto.insertar_producto(
                nombre=nombre,
                descripcion=descripcion,
                categorias_id=categorias_id,
                precio=precio,
                stock=stock,
                destacado=destacado,
                imagen=imagen_filename
            )
            flash('Producto agregado con éxito', 'success')
        except Exception as e:
            flash('Error al agregar el producto: ' + str(e), 'error')
        return redirect(url_for('admin_productos'))

    categorias = controlador_categorias.obtener_todas_categorias()
    return render_template('admin/nuevo_producto.html', categorias=categorias)

@app.route('/admin/editar_producto/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_producto(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categorias_id = request.form['categorias_id']
        precio = request.form['precio']
        stock = request.form['stock']
        destacado = 1 if 'destacado' in request.form else 0

        # Procesar la imagen
        imagen = request.files['imagen']
        imagen_filename = producto.imagen  # Mantener la imagen existente si no se carga una nueva
        
        if imagen and allowed_file(imagen.filename):
            try:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(UPLOAD_FOLDER, imagen_filename))
            except Exception as e:
                flash('Error al cargar la imagen: ' + str(e), 'error')
                return redirect(url_for('admin_editar_producto', id=id))
        
        # Actualiza el producto en la base de datos
        try:
            controlador_producto.actualizar_producto(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                categorias_id=categorias_id,
                imagen=imagen_filename
            )
            flash('Producto actualizado con éxito', 'success')
        except Exception as e:
            flash('Error al actualizar el producto: ' + str(e), 'error')

        return redirect(url_for('admin_productos'))

    categorias = controlador_categorias.obtener_todas_categorias()
    return render_template('admin/editar_producto.html', producto=producto, categorias=categorias)

@app.route('/admin/producto/eliminar/<int:id>', methods=['POST'])
@admin_required
def admin_eliminar_producto(id):
    controlador_producto.eliminar_producto(id)
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('admin_productos'))

@app.route('/admin/pedidos')
@admin_required
def admin_pedidos():
    pedidos = controlador_pedido.obtener_todos_pedidos()
    return render_template('admin/pedidos.html', pedidos=pedidos)

@app.route('/admin/pedido/<int:id>')
@admin_required
def admin_detalle_pedido(id):
    pedido = controlador_pedido.obtener_pedido_por_id(id)
    return render_template('admin/detalle_pedido.html', pedido=pedido)

@app.route('/admin/pedido/actualizar-estado/<int:id>', methods=['POST'])
@admin_required
def admin_actualizar_estado_pedido(id):
    nuevo_estado = request.form.get('nuevo_estado')
    controlador_pedido.actualizar_estado_pedido(id, nuevo_estado)
    flash('Estado del pedido actualizado con éxito', 'success')
    return redirect(url_for('admin_detalle_pedido', id=id))

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
    return render_template('admin/editar_categorias.html')

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

@app.route('/admin/usuario/<int:id>')
@admin_required
def admin_detalle_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template('admin/detalle_usuario.html', usuario=usuario)

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
                flash('Contraseña actualizada correctamente', 'success')
                return redirect(url_for('mi_cuenta'))
            else:
                flash('Las contraseñas nuevas no coinciden', 'error')
        else:
            flash('La contraseña actual es incorrecta', 'error')
    
    return render_template('cambiar_contrasena.html')

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
