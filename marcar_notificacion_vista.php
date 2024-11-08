<?php
header('Content-Type: application/json');
require_once 'controlador_notificaciones.php';

try {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Método no permitido');
    }
    
    if (!isset($_POST['notificacion_id'])) {
        throw new Exception('ID de notificación no proporcionado');
    }
    
    $resultado = marcarNotificacionComoVista($_POST['notificacion_id']);
    
    if ($resultado) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'error' => 'No se pudo marcar la notificación como vista']);
    }
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}