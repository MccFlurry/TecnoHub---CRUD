document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality for the admin panel here
    console.log('Admin panel loaded');

    // Example: Toggle mobile menu
    const menuButton = document.querySelector('#mobile-menu-button');
    const sidebar = document.querySelector('#sidebar');

    if (menuButton && sidebar) {
        menuButton.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
        });
    }

});

//detalle_pedido

document.addEventListener('DOMContentLoaded', function () {
    const btnActualizarEstado = document.getElementById('btn-actualizar-estado');
    const formActualizarEstado = document.getElementById('actualizar-estado-form');

    if (btnActualizarEstado) {
        btnActualizarEstado.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas actualizar el estado del pedido?');
            if (confirmacion) {
                formActualizarEstado.submit();
            }
        });
    }
});

//editar_pedido
document.addEventListener('DOMContentLoaded', function () {
    const btnGuardarCambios = document.getElementById('btn-guardar-cambios');
    const formEditarPedido = document.getElementById('editar-pedido-form');

    if (btnGuardarCambios) {
        btnGuardarCambios.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas guardar los cambios del pedido?');
            if (confirmacion) {
                formEditarPedido.submit();
            }
        });
    }
});

//editar_nueva_categoria
document.addEventListener('DOMContentLoaded', function () {
    const btnGuardarCategoria = document.getElementById('btn-guardar-categoria');
    const formCategoria = document.getElementById('categoria-form');

    if (btnGuardarCategoria) {
        btnGuardarCategoria.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas guardar los cambios en la categoría?');
            if (confirmacion) {
                formCategoria.submit();
            }
        });
    }
});

//editar_nuevo_producto
document.addEventListener('DOMContentLoaded', function () {
    const btnGuardarProducto = document.getElementById('btn-guardar-producto');
    const formProducto = document.querySelector('form');

    if (btnGuardarProducto) {
        btnGuardarProducto.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas guardar los cambios en el producto?');
            if (confirmacion) {
                formProducto.submit();
            }
        });
    }
});

//editar_usuario
document.addEventListener('DOMContentLoaded', function () {
    const btnGuardarUsuario = document.getElementById('btn-guardar-usuario');
    const formEditarUsuario = document.querySelector('form');

    if (btnGuardarUsuario) {
        btnGuardarUsuario.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas guardar los cambios del usuario?');
            if (confirmacion) {
                formEditarUsuario.submit();
            }
        });
    }
});

//categorias
document.addEventListener('DOMContentLoaded', function () {
    // Confirmación al añadir nueva categoría
    const btnNuevaCategoria = document.getElementById('btn-nueva-categoria');
    if (btnNuevaCategoria) {
        btnNuevaCategoria.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas añadir una nueva categoría?');
            if (!confirmacion) {
                event.preventDefault();  // Cancela la redirección si el usuario no confirma
            }
        });
    }

    // Confirmación al editar categoría
    const botonesEditar = document.querySelectorAll('.editar-categoria-btn');
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas editar esta categoría?');
            if (!confirmacion) {
                event.preventDefault();  // Cancela la navegación si el usuario no confirma
            }
        });
    });

    // Confirmación al eliminar categoría
    const botonesEliminar = document.querySelectorAll('.eliminar-categoria-btn');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que quieres eliminar esta categoría? Esta acción no se puede deshacer.');
            if (confirmacion) {
                boton.closest('.eliminar-categoria-form').submit();
            }
        });
    });
});

//pedidos
document.addEventListener('DOMContentLoaded', function () {
    // Confirmación al editar un pedido
    const botonesEditar = document.querySelectorAll('.editar-pedido-btn');
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas editar este pedido?');
            if (confirmacion) {
                boton.closest('.editar-pedido-form').submit();
            }
        });
    });

    // Confirmación al eliminar un pedido
    const botonesEliminar = document.querySelectorAll('.eliminar-pedido-btn');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas eliminar este pedido? Esta acción no se puede deshacer.');
            if (confirmacion) {
                boton.closest('.eliminar-pedido-form').submit();
            }
        });
    });
});

//productos
document.addEventListener('DOMContentLoaded', function () {
    // Confirmación al añadir nuevo producto
    const btnNuevoProducto = document.getElementById('btn-nuevo-producto');
    if (btnNuevoProducto) {
        btnNuevoProducto.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas añadir un nuevo producto?');
            if (!confirmacion) {
                event.preventDefault();  // Cancela la acción si no se confirma
            }
        });
    }

    // Confirmación al editar un producto
    const botonesEditar = document.querySelectorAll('.editar-producto-btn');
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas editar este producto?');
            if (!confirmacion) {
                event.preventDefault();  // Cancela la acción si no se confirma
            }
        });
    });

    // Confirmación al eliminar un producto
    const botonesEliminar = document.querySelectorAll('.eliminar-producto-btn');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.');
            if (confirmacion) {
                boton.closest('.eliminar-producto-form').submit();
            }
        });
    });
});

//usuarios
document.addEventListener('DOMContentLoaded', function () {
    // Confirmación al editar un usuario
    const botonesEditar = document.querySelectorAll('.editar-usuario-btn');
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function (event) {
            const confirmacion = confirm('¿Estás seguro de que deseas editar este usuario?');
            if (!confirmacion) {
                event.preventDefault();  // Cancela la acción si no se confirma
            }
        });
    });

    // Confirmación al eliminar un usuario
    const botonesEliminar = document.querySelectorAll('.eliminar-usuario-btn');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', function () {
            const confirmacion = confirm('¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.');
            if (confirmacion) {
                boton.closest('.eliminar-usuario-form').submit();
            }
        });
    });
});
