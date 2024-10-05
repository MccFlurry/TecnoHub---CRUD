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
    let envio = 5; // costo de envío fijo
    document.getElementById('envio').textContent = `S/${envio.toFixed(2)}`;
    let total = subtotal + envio;
    document.getElementById('total').textContent = `S/${total.toFixed(2)}`;

    let irAPagarBtn = document.getElementById('irAPagarBtn');
    if (carrito.length === 0) {
        irAPagarBtn.classList.add('disabled');
        irAPagarBtn.onclick = (e) => e.preventDefault();
    } else {
        irAPagarBtn.classList.remove('disabled');
        irAPagarBtn.onclick = null;
    }
}
