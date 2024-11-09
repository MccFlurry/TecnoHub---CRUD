document.addEventListener("DOMContentLoaded", () => {
    function formatearFecha(fechaStr) {
        const fecha = new Date(fechaStr);
        return fecha.toLocaleString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function marcarComoVisto(notificacionId, elemento) {
        const formData = new FormData();
        formData.append('notificacion_id', notificacionId);

        fetch('../../marcar_notificacion_vista.php', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Añadir clase de transición
                elemento.classList.add('opacity-0', 'transition-all', 'duration-300');
                
                // Esperar a que termine la transición antes de remover
                setTimeout(() => {
                    elemento.remove();
                    
                    // Verificar si quedan notificaciones
                    if (document.getElementById('notificaciones-list').children.length === 0) {
                        document.getElementById('notificaciones-list').innerHTML = `
                            <li class="p-4 text-center text-gray-500">
                                No hay notificaciones nuevas
                            </li>
                        `;
                    }
                }, 300);
            } else {
                throw new Error(data.error || 'Error al marcar como vista');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al marcar la notificación como vista');
        });
    }

    function obtenerNotificaciones() {
        fetch('../../obtener_notificaciones.php')
            .then(response => response.json())
            .then(data => {
                const notificacionesList = document.getElementById('notificaciones-list');
                notificacionesList.innerHTML = '';

                if (data.length === 0) {
                    notificacionesList.innerHTML = `
                        <li class="p-4 text-center text-gray-500">
                            No hay notificaciones nuevas
                        </li>
                    `;
                    return;
                }

                data.forEach(notificacion => {
                    const li = document.createElement('li');
                    li.className = 'p-4 transition-all duration-300 ease-in-out hover:bg-gray-50';
                    li.id = `notificacion-${notificacion.id}`;

                    li.innerHTML = `
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <div class="flex-shrink-0">
                                    <img class="w-10 h-10 rounded-full object-cover" 
                                         src="/static/img/${notificacion.usuario_foto || 'default.jpg'}" 
                                         alt="${notificacion.usuario_nombre}"
                                         onerror="this.src='/static/img/default.jpg'">
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-gray-900">
                                        ${notificacion.usuario_nombre}
                                    </p>
                                    <p class="text-sm text-gray-500">
                                        ${notificacion.mensaje}
                                    </p>
                                    <p class="text-xs text-gray-400">
                                        ${formatearFecha(notificacion.fecha_creacion)}
                                    </p>
                                </div>
                            </div>
                            <div class="ml-4">
                                <button onclick="event.preventDefault(); marcarComoVisto(${notificacion.id}, this.closest('li'))"
                                        class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200">
                                    Marcar como vista
                                </button>
                            </div>
                        </div>
                    `;

                    notificacionesList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('notificaciones-list').innerHTML = `
                    <li class="p-4 text-center text-red-500">
                        Error al cargar las notificaciones. Por favor, intente nuevamente.
                    </li>
                `;
            });
    }

    window.marcarComoVisto = marcarComoVisto;

    obtenerNotificaciones();
    
    setInterval(obtenerNotificaciones, 5000);
});