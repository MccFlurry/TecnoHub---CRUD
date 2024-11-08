<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notificaciones</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container px-4 py-8 mx-auto">
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-gray-900">Notificaciones</h1>
        </div>

        <div id="notificaciones-container" class="bg-white rounded-lg shadow">
            <ul id="notificaciones-list" class="divide-y divide-gray-200">
                <!-- Las notificaciones se cargarán dinámicamente aquí -->
            </ul>
        </div>
    </div>

    <script src="/static/js/notificaciones.js"></script>
</body>
</html>