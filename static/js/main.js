document.addEventListener('DOMContentLoaded', function () {
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

    // Nueva funcionalidad para el carrito dinámico
    const carritoTabla = document.getElementById('carrito-tabla');
    if (carritoTabla) {
        // Manejar cambios en las cantidades
        carritoTabla.querySelectorAll('.cantidad-input').forEach(input => {
            let timeoutId;
            
            input.addEventListener('change', (e) => {
                const fila = e.target.closest('tr');
                const productoId = fila.dataset.productoId;
                const precio = parseFloat(fila.querySelector('[data-precio]').dataset.precio);
                const cantidad = parseInt(e.target.value);
                
                // Actualizar subtotal visual inmediatamente
                const subtotalElement = fila.querySelector('.subtotal');
                const subtotal = (precio * cantidad).toFixed(2);
                subtotalElement.textContent = `S/.${subtotal}`;
                
                // Debounce la actualización en el servidor
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    actualizarCantidadCarrito(productoId, cantidad);
                }, 500);
            });
        });

        // Manejar clicks en botones de eliminar
        carritoTabla.querySelectorAll('.eliminar-item').forEach(button => {
            button.addEventListener('click', async (e) => {
                const productoId = e.target.dataset.productoId;
                const fila = e.target.closest('tr');
                await eliminarItemCarrito(productoId, fila);
            });
        });
    }
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

async function actualizarCantidadCarrito(productoId, cantidad) {
    try {
        const formData = new FormData();
        formData.append('producto_id', productoId);
        formData.append('cantidad', cantidad);

        window.location.href = '/carrito';
        
    } catch (error) {
        console.error('Error:', error);
        window.location.href = '/carrito';
    }
}

async function eliminarItemCarrito(productoId, fila) {
    try {
        window.location.href = `/eliminar-del-carrito/${productoId}`;
    } catch (error) {
        console.error('Error:', error);
        window.location.href = '/carrito';
    }
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
    const notificacionesContainer = document.getElementById('notificaciones');
    
    const notificacion = document.createElement('div');
    notificacion.classList.add(
        'mb-4',
        'p-4',
        'rounded-lg',
        'shadow-lg',
        'transform',
        'transition-all',
        'duration-300',
        'translate-x-full',
        tipo === 'success' ? 'bg-green-500' : 'bg-red-500',
        'text-white'
    );
    notificacion.textContent = mensaje;

    notificacionesContainer.appendChild(notificacion);

    // Trigger animation
    setTimeout(() => {
        notificacion.classList.remove('translate-x-full');
    }, 10);

    // Remove notification after delay
    setTimeout(() => {
        notificacion.classList.add('translate-x-full');
        setTimeout(() => {
            notificacion.remove();
        }, 300);
    }, 3000);
}

// Inicializar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Animación de fade-in para elementos
    const fadeElems = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    });

    fadeElems.forEach(elem => observer.observe(elem));
});

// Manejo del menú móvil
document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function (event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
});

// Manejo del menú de usuario
document.addEventListener('DOMContentLoaded', function () {
    const userButton = document.querySelector('[data-menu="user"]');
    const userMenu = document.querySelector('[data-menu-content="user"]');

    if (userButton && userMenu) {
        userButton.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            userMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function (event) {
            if (!userButton.contains(event.target) && !userMenu.contains(event.target)) {
                userMenu.classList.add('hidden');
            }
        });
    }
});

// Manejo del menú de categorías
document.addEventListener('DOMContentLoaded', function () {
    const categoriasButton = document.querySelector('[data-menu="categorias"]');
    const categoriasMenu = document.querySelector('[data-menu-content="categorias"]');

    if (categoriasButton && categoriasMenu) {
        categoriasButton.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            categoriasMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function (event) {
            if (!categoriasButton.contains(event.target) && !categoriasMenu.contains(event.target)) {
                categoriasMenu.classList.add('hidden');
            }
        });
    }
});

// Manejo del formulario de búsqueda
document.addEventListener('DOMContentLoaded', function () {
    const campoBusqueda = document.getElementById('busqueda');
    const formBusqueda = document.querySelector('form[action="/buscar"]');

    if (campoBusqueda && formBusqueda) {
        campoBusqueda.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                formBusqueda.submit();
            }
        });
    }
});

// Manejo de favoritos
document.addEventListener('DOMContentLoaded', function() {
    const favButton = document.getElementById('fav-button');
    if (favButton) {
        favButton.addEventListener('click', manejarFavorito);
    }
});

function manejarFavorito(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const productoId = button.dataset.productoId;
    const icon = button.querySelector('#fav-icon');
    const esFavorito = icon.classList.contains('text-red-500');

    // Añadir efecto de pulsación
    button.classList.add('scale-90');
    setTimeout(() => button.classList.remove('scale-90'), 150);

    // Realizar la petición al servidor
    fetch(`/${esFavorito ? 'eliminar' : 'agregar'}-favorito/${productoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (esFavorito) {
                // Cambiar a corazón vacío
                icon.classList.remove('text-red-500', 'animate-favorite');
                icon.classList.add('text-gray-400', 'hover:text-red-500');
                mostrarNotificacion('Eliminado de favoritos', 'info');
            } else {
                // Cambiar a corazón lleno
                icon.classList.remove('text-gray-400', 'hover:text-red-500');
                icon.classList.add('text-red-500', 'animate-favorite');
                mostrarNotificacion('Agregado a favoritos', 'success');
                animarCorazon(icon);
            }
        } else {
            mostrarNotificacion(data.message || 'Error al procesar la solicitud', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarNotificacion('Error al procesar la solicitud', 'error');
    });
}

function animarCorazon(icon) {
    icon.animate([
        { transform: 'scale(1)' },
        { transform: 'scale(1.3)' },
        { transform: 'scale(1)' }
    ], {
        duration: 500,
        easing: 'ease-in-out'
    });
}

function mostrarNotificacion(mensaje, tipo) {
    const notificacion = document.createElement('div');
    notificacion.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg transition-all transform translate-y-0 z-50 ${
        tipo === 'success' ? 'bg-green-500' :
        tipo === 'error' ? 'bg-red-500' :
        'bg-blue-500'
    } text-white`;
    
    notificacion.textContent = mensaje;
    document.body.appendChild(notificacion);

    // Entrada con animación
    notificacion.animate([
        { transform: 'translateY(-100%)', opacity: 0 },
        { transform: 'translateY(0)', opacity: 1 }
    ], {
        duration: 300,
        easing: 'ease-out'
    });

    // Remover después de 3 segundos
    setTimeout(() => {
        notificacion.animate([
            { transform: 'translateY(0)', opacity: 1 },
            { transform: 'translateY(-100%)', opacity: 0 }
        ], {
            duration: 300,
            easing: 'ease-in'
        }).onfinish = () => notificacion.remove();
    }, 3000);
}

// Funcionalidad Arma tu Kit
document.addEventListener('DOMContentLoaded', function () {
    const celularSelect = document.getElementById('celular-select');
    const smartwatchSelect = document.getElementById('smartwatch-select');
    const accesorioSelect = document.getElementById('accesorio-select');

    const celularSeleccionado = document.getElementById('celular-seleccionado');
    const smartwatchSeleccionado = document.getElementById('smartwatch-seleccionado');
    const accesorioSeleccionado = document.getElementById('accesorio-seleccionado');
    const totalKit = document.getElementById('total-kit');

    function actualizarResumen() {
        if (celularSelect && smartwatchSelect && accesorioSelect) {
            const celularOption = celularSelect.options[celularSelect.selectedIndex];
            const smartwatchOption = smartwatchSelect.options[smartwatchSelect.selectedIndex];
            const accesorioOption = accesorioSelect.options[accesorioSelect.selectedIndex];

            if (celularSeleccionado && smartwatchSeleccionado && accesorioSeleccionado && totalKit) {
                celularSeleccionado.textContent = celularOption.text.includes('-') ? celularOption.text.split('-')[0].trim() : 'Ninguno';
                smartwatchSeleccionado.textContent = smartwatchOption.text.includes('-') ? smartwatchOption.text.split('-')[0].trim() : 'Ninguno';
                accesorioSeleccionado.textContent = accesorioOption.text.includes('-') ? accesorioOption.text.split('-')[0].trim() : 'Ninguno';

                const total = parseFloat(celularOption.getAttribute('data-precio') || 0) +
                    parseFloat(smartwatchOption.getAttribute('data-precio') || 0) +
                    parseFloat(accesorioOption.getAttribute('data-precio') || 0);

                totalKit.textContent = total.toFixed(2);
            }
        }
    }

    if (celularSelect && smartwatchSelect && accesorioSelect) {
        celularSelect.addEventListener('change', actualizarResumen);
        smartwatchSelect.addEventListener('change', actualizarResumen);
        accesorioSelect.addEventListener('change', actualizarResumen);
    }
});

// Función para cerrar mensajes flash
function closeFlashMessage(messageId) {
    const flashMessage = document.getElementById(messageId);
    if (flashMessage) {
        flashMessage.classList.remove('slide-in');
        flashMessage.classList.add('slide-out');
        setTimeout(() => {
            flashMessage.remove();
        }, 500);
    }
}

// Inicialización de mensajes flash
window.addEventListener('load', function() {
    const flashMessages = document.querySelectorAll('[id^="flashMessage-"]');
    flashMessages.forEach(message => {
        setTimeout(() => {
            closeFlashMessage(message.id);
        }, 5000);
    });
});

// Funciones de utilidad para validación
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Smooth scroll para enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Inicializar observador de intersección para animaciones
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observerOptions = {
        root: null,
        threshold: 0.1,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(element => {
        observer.observe(element);
    });
});

// Gestión de estado de carga
window.addEventListener('load', function() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
});

// Manejo de errores global
window.addEventListener('error', function(e) {
    console.error('Error global:', e.error);
    mostrarNotificacion('Ha ocurrido un error inesperado', 'error');
});

// Prevenir reenvío de formularios
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});