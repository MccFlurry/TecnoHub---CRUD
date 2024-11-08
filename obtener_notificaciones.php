<?php
header('Content-Type: application/json');
require_once 'controlador_notificaciones.php';

try {
    $notificaciones = obtenerNotificaciones();
    echo json_encode($notificaciones);
} catch (Exception $e) {
    error_log("Error: " . $e->getMessage());
    http_response_code(500);
    echo json_encode(['error' => 'Error interno del servidor']);
}