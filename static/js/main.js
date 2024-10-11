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

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar los tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

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

    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Validación de formulario de suscripción
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (validateEmail(email)) {
                alert('¡Gracias por suscribirte!');
                this.reset();
            } else {
                alert('Por favor, ingresa un email válido.');
            }
        });
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});

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
});

document.addEventListener('DOMContentLoaded', function() {
    const userButton = document.querySelector('[data-menu="user"]');
    const userMenu = document.querySelector('[data-menu-content="user"]');

    if (userButton && userMenu) {
        userButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            userMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(event) {
            if (!userButton.contains(event.target) && !userMenu.contains(event.target)) {
                userMenu.classList.add('hidden');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Función para encontrar el botón de categorías
    function findCategoriasButton() {
        const buttons = document.querySelectorAll('button');
        for (let button of buttons) {
            if (button.textContent.trim().toLowerCase().includes('categorías')) {
                return button;
            }
        }
        return document.querySelector('[data-menu="categorias"]');
    }

    // Función para encontrar el menú de categorías
    function findCategoriasMenu(button) {
        if (button) {
            const parent = button.closest('.relative, .group');
            return parent ? parent.querySelector('.absolute, [data-menu-content="categorias"]') : null;
        }
        return document.querySelector('[data-menu-content="categorias"]');
    }

    const categoriasButton = findCategoriasButton();
    const categoriasMenu = findCategoriasMenu(categoriasButton);

    if (categoriasButton && categoriasMenu) {
        categoriasButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            categoriasMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(event) {
            if (!categoriasButton.contains(event.target) && !categoriasMenu.contains(event.target)) {
                categoriasMenu.classList.add('hidden');
            }
        });
    } else {
        console.warn('No se encontró el botón de categorías o el menú de categorías');
        console.log('Botón de categorías:', categoriasButton);
        console.log('Menú de categorías:', categoriasMenu);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const campoBusqueda = document.getElementById('busqueda'); // Cambia 'busqueda' por el id correcto del input de búsqueda
    const formBusqueda = document.querySelector('form[action="/buscar"]'); // Asegúrate de que el form apunta a la ruta correcta

    if (campoBusqueda && formBusqueda) {
        campoBusqueda.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault(); // Prevenir el comportamiento por defecto
                formBusqueda.submit(); // Enviar el formulario al servidor
            }
        });
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const favButton = document.getElementById('fav-button');
    const favIcon = document.getElementById('fav-icon');

    if (favButton) {
        favButton.addEventListener('click', function () {
            const productoId = favButton.getAttribute('data-producto-id');
            const isFavorito = favIcon.classList.contains('text-red-500');
            const url = isFavorito ? `/eliminar-favorito/${productoId}` : `/agregar-favorito/${productoId}`;

            console.log('Enviando solicitud a:', url);  // Verifica si la URL es correcta

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ producto_id: productoId })
            })
            .then(response => {
                console.log('Respuesta recibida:', response);
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data);  // Imprimir los datos recibidos
                if (data.success) {
                    if (isFavorito) {
                        favIcon.classList.remove('text-red-500');
                        favIcon.classList.add('text-gray-500');
                        alert('Producto eliminado de tus favoritos');
                    } else {
                        favIcon.classList.remove('text-gray-500');
                        favIcon.classList.add('text-red-500');
                        alert('Producto añadido a tus favoritos');
                    }
                } else {
                    alert(`Error: ${data.message || 'Hubo un error, inténtalo nuevamente.'}`);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud, inténtalo nuevamente.');
            });
        });
    }
});
