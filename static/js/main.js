document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidad para el carrito de compras
    const botonesAgregarCarrito = document.querySelectorAll('.agregar-carrito');
    botonesAgregarCarrito.forEach(boton => {
        boton.addEventListener('click', agregarAlCarrito);
    });

    // Funcionalidad para la búsqueda en tiempo real
    const campoBusqueda = document.getElementById('busqueda');
    if (campoBusqueda) {
        campoBusqueda.addEventListener('input', busquedaEnTiempoReal);
    }

    // Funcionalidad para el toggle del menú en dispositivos móviles
    const botonMenu = document.getElementById('toggle-menu');
    const menuPrincipal = document.getElementById('menu-principal');
    if (botonMenu && menuPrincipal) {
        botonMenu.addEventListener('click', toggleMenu);
    }

    // Inicializar tooltips
    inicializarTooltips();

    // Validación de formularios
    const formularios = document.querySelectorAll('form');
    formularios.forEach(form => {
        form.addEventListener('submit', validarFormulario);
    });
});

function agregarAlCarrito(event) {
    event.preventDefault();
    const boton = event.target;
    const productoId = boton.getAttribute('data-producto-id');
    const cantidad = document.querySelector(`#cantidad-${productoId}`).value;

    fetch('/agregar-al-carrito', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ producto_id: productoId, cantidad: cantidad }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            actualizarContadorCarrito(data.total_items);
            mostrarNotificacion('Producto agregado al carrito', 'success');
        } else {
            mostrarNotificacion('Error al agregar el producto', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al procesar la solicitud', 'error');
    });
}

function busquedaEnTiempoReal() {
    const query = this.value.toLowerCase();
    const productos = document.querySelectorAll('.producto-card');

    productos.forEach(producto => {
        const nombre = producto.querySelector('h3').textContent.toLowerCase();
        if (nombre.includes(query)) {
            producto.style.display = 'block';
        } else {
            producto.style.display = 'none';
        }
    });
}

function toggleMenu() {
    menuPrincipal.classList.toggle('active');
}

function inicializarTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', mostrarTooltip);
        tooltip.addEventListener('mouseleave', ocultarTooltip);
    });
}

function mostrarTooltip(event) {
    const tooltip = event.target;
    const tooltipText = tooltip.getAttribute('data-tooltip');
    
    const tooltipElement = document.createElement('div');
    tooltipElement.classList.add('tooltip');
    tooltipElement.textContent = tooltipText;
    
    document.body.appendChild(tooltipElement);
    
    const rect = tooltip.getBoundingClientRect();
    tooltipElement.style.top = `${rect.bottom + window.scrollY + 5}px`;
    tooltipElement.style.left = `${rect.left + window.scrollX}px`;
}

function ocultarTooltip() {
    const tooltipElement = document.querySelector('.tooltip');
    if (tooltipElement) {
        tooltipElement.remove();
    }
}

function validarFormulario(event) {
    const form = event.target;
    const camposRequeridos = form.querySelectorAll('[required]');
    let formValido = true;

    camposRequeridos.forEach(campo => {
        if (!campo.value.trim()) {
            formValido = false;
            mostrarErrorCampo(campo, 'Este campo es requerido');
        } else {
            limpiarErrorCampo(campo);
        }
    });

    if (!formValido) {
        event.preventDefault();
    }
}

function mostrarErrorCampo(campo, mensaje) {
    limpiarErrorCampo(campo);
    const errorElement = document.createElement('div');
    errorElement.classList.add('error-mensaje');
    errorElement.textContent = mensaje;
    campo.parentNode.appendChild(errorElement);
    campo.classList.add('campo-error');
}

function limpiarErrorCampo(campo) {
    const errorElement = campo.parentNode.querySelector('.error-mensaje');
    if (errorElement) {
        errorElement.remove();
    }
    campo.classList.remove('campo-error');
}

function actualizarContadorCarrito(totalItems) {
    const contadorCarrito = document.getElementById('contador-carrito');
    if (contadorCarrito) {
        contadorCarrito.textContent = totalItems;
    }
}

function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.createElement('div');
    notificacion.classList.add('notificacion', `notificacion-${tipo}`);
    notificacion.textContent = mensaje;
    
    document.body.appendChild(notificacion);
    
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 10);
    
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            notificacion.remove();
        }, 300);
    }, 3000);
}   