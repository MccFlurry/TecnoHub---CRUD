//CARRITO DE COMPRAS
function obtenerCarrito() {
    let carrito = localStorage.getItem('carrito');
    if (carrito) {
        return JSON.parse(carrito);
    } else {
        return [];
    }
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function agregarProductoAlCarrito(producto) {
    let carrito = obtenerCarrito();
    let productoExistente = carrito.find(p => p.nombre === producto.nombre);
    if (productoExistente) {
        productoExistente.cantidad += producto.cantidad;
    } else {
        carrito.push(producto);
    }
    guardarCarrito(carrito);
    alert('Producto agregado al carrito');
}

document.addEventListener('DOMContentLoaded', function() {
    let botonAgregarCarrito = document.getElementById('agregarCarrito');
    if (botonAgregarCarrito) {
        botonAgregarCarrito.addEventListener('click', function() {
            let nombreProducto = document.querySelector('h2').textContent;
            let precioProducto = parseFloat(document.querySelector('h5').textContent.replace('S/', '').trim());
            let cantidadProducto = parseInt(document.getElementById('cantidad').value);

            let producto = {
                nombre: nombreProducto,
                precio: precioProducto,
                cantidad: cantidadProducto
            };

            agregarProductoAlCarrito(producto);
        });
    }

    if (window.location.pathname.includes('carrito.html')) {
        actualizarCarritoPagina();
    }
});

function actualizarCarritoPagina() {
    let carrito = obtenerCarrito();
    let carritoTabla = document.getElementById('carritoTabla');
    let subtotal = 0;

    carritoTabla.innerHTML = '';

    carrito.forEach((producto, index) => {
        let fila = document.createElement('tr');

        let celdaNombre = document.createElement('td');
        celdaNombre.textContent = producto.nombre;

        let celdaPrecio = document.createElement('td');
        celdaPrecio.textContent = `S/${producto.precio}`;

        let celdaCantidad = document.createElement('td');
        celdaCantidad.textContent = producto.cantidad;

        let celdaSubtotal = document.createElement('td');
        let subtotalProducto = producto.precio * producto.cantidad;
        celdaSubtotal.textContent = `S/${subtotalProducto.toFixed(2)}`;
        subtotal += subtotalProducto;

        let celdaEliminar = document.createElement('td');
        let botonEliminar = document.createElement('button');
        botonEliminar.textContent = 'Eliminar';
        botonEliminar.className = 'btn btn-danger';
        botonEliminar.onclick = () => {
            carrito.splice(index, 1);
            guardarCarrito(carrito);
            actualizarCarritoPagina();
        };
        celdaEliminar.appendChild(botonEliminar);

        fila.appendChild(celdaNombre);
        fila.appendChild(celdaPrecio);
        fila.appendChild(celdaCantidad);
        fila.appendChild(celdaSubtotal);
        fila.appendChild(celdaEliminar);

        carritoTabla.appendChild(fila);
    });

    document.getElementById('subtotal').textContent = `S/${subtotal.toFixed(2)}`;
    let envio = 5; // costo de envío fijo
    document.getElementById('envio').textContent = `S/${envio.toFixed(2)}`;
    let total = subtotal + envio;
    document.getElementById('total').textContent = `S/${total.toFixed(2)}`;

    let irAPagarBtn = document.querySelector('.btn-primary');
    if (carrito.length === 0) {
        irAPagarBtn.classList.add('disabled');
        irAPagarBtn.onclick = (e) => e.preventDefault();
    } else {
        irAPagarBtn.classList.remove('disabled');
        irAPagarBtn.onclick = null;
    }
}


//ARMA TU KIT
let productosSeleccionados = [];

function agregarProductoKit(nombre, precio, imgSrc) {
    const producto = { nombre, precio, cantidad: 1, imgSrc };
    const index = productosSeleccionados.findIndex(p => p.nombre === nombre);

    if (index === -1) {
        productosSeleccionados.push(producto);
    } else {
        productosSeleccionados[index].cantidad += 1;
    }
    
    actualizarListaProductosSeleccionados();
}

function actualizarListaProductosSeleccionados() {
    const contenedores = {
        'Xiaomi Mi 11 Lite': 'productosSeleccionadosCelular',
        'Samsung S24 Ultra': 'productosSeleccionadosCelular',
        'iPhone 15': 'productosSeleccionadosCelular',
        'Case Negro': 'productosSeleccionadosFunda',
        'Case Rojo': 'productosSeleccionadosFunda',
        'Case Verde': 'productosSeleccionadosFunda',
        'Sony WH-CH520': 'productosSeleccionadosAudifonos',
        'Philips TAH8506BK/00': 'productosSeleccionadosAudifonos',
        'Hoco TWS EW05': 'productosSeleccionadosAudifonos'
    };

    for (const contenedor in contenedores) {
        document.getElementById(contenedores[contenedor]).innerHTML = '';
    }

    productosSeleccionados.forEach((producto, index) => {
        const contenedorID = contenedores[producto.nombre];
        if (contenedorID) {
            const productosDiv = document.getElementById(contenedorID);

            const productoElem = document.createElement('div');
            productoElem.className = 'producto-seleccionado d-flex justify-content-between align-items-center mb-3';

            productoElem.innerHTML = `
                <div class="d-flex align-items-center">
                    <img src="${producto.imgSrc}" style="height: 50px; width: auto;" class="img-fluid" alt="">
                    <div class="ms-3">
                        <p>${producto.nombre}</p>
                        <p>S/${producto.precio}</p>
                    </div>
                </div>
                <div class="d-flex align-items-center">
                    <input type="number" class="form-control" value="${producto.cantidad}" min="1" style="width: 60px;" onchange="cambiarCantidad(${index}, this.value)">
                    <button class="btn btn-danger ms-3" onclick="eliminarProductoSeleccionado(${index})">Eliminar</button>
                </div>
            `;

            productosDiv.appendChild(productoElem);
        }
    });

    actualizarTotal();
}

function cambiarCantidad(index, cantidad) {
    productosSeleccionados[index].cantidad = parseInt(cantidad);
    actualizarTotal();
}

function eliminarProductoSeleccionado(index) {
    productosSeleccionados.splice(index, 1);
    actualizarListaProductosSeleccionados();
}

function actualizarTotal() {
    let total = 0;
    productosSeleccionados.forEach(producto => {
        total += producto.precio * producto.cantidad;
    });
    document.getElementById('total-price').innerText = total.toFixed(2);
}

function añadirProductosAlCarrito() {
    let carrito = obtenerCarrito();
    productosSeleccionados.forEach(producto => {
        let productoExistente = carrito.find(p => p.nombre === producto.nombre);
        if (productoExistente) {
            productoExistente.cantidad += producto.cantidad;
        } else {
            carrito.push(producto);
        }
    });
    guardarCarrito(carrito);
    alert('Productos agregados al carrito');
}

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('carrito.html')) {
        actualizarCarritoPagina();
    }
});

function obtenerCarrito() {
    let carrito = localStorage.getItem('carrito');
    if (carrito) {
        return JSON.parse(carrito);
    } else {
        return [];
    }
}

function guardarCarrito(carrito) {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

function actualizarCarritoPagina() {
    let carrito = obtenerCarrito();
    let carritoTabla = document.getElementById('carritoTabla');
    let subtotal = 0;

    carritoTabla.innerHTML = '';

    carrito.forEach((producto, index) => {
        let fila = document.createElement('tr');

        let celdaNombre = document.createElement('td');
        celdaNombre.textContent = producto.nombre;

        let celdaPrecio = document.createElement('td');
        celdaPrecio.textContent = `S/${producto.precio}`;

        let celdaCantidad = document.createElement('td');
        celdaCantidad.textContent = producto.cantidad;

        let celdaSubtotal = document.createElement('td');
        let subtotalProducto = producto.precio * producto.cantidad;
        celdaSubtotal.textContent = `S/${subtotalProducto.toFixed(2)}`;
        subtotal += subtotalProducto;

        let celdaEliminar = document.createElement('td');
        let botonEliminar = document.createElement('button');
        botonEliminar.textContent = 'Eliminar';
        botonEliminar.className = 'btn btn-danger';
        botonEliminar.onclick = () => {
            carrito.splice(index, 1);
            guardarCarrito(carrito);
            actualizarCarritoPagina();
        };
        celdaEliminar.appendChild(botonEliminar);

        fila.appendChild(celdaNombre);
        fila.appendChild(celdaPrecio);
        fila.appendChild(celdaCantidad);
        fila.appendChild(celdaSubtotal);
        fila.appendChild(celdaEliminar);

        carritoTabla.appendChild(fila);
    });

    document.getElementById('subtotal').textContent = `S/${subtotal.toFixed(2)}`;
    let envio = 5;
    document.getElementById('envio').textContent = `S/${envio.toFixed(2)}`;
    let total = subtotal + envio;
    document.getElementById('total').textContent = `S/${total.toFixed(2)}`;

    let irAPagarBtn = document.querySelector('.btn-primary');
    if (carrito.length === 0) {
        irAPagarBtn.classList.add('disabled');
        irAPagarBtn.onclick = (e) => e.preventDefault();
    } else {
        irAPagarBtn.classList.remove('disabled');
        irAPagarBtn.onclick = null;
    }
}
