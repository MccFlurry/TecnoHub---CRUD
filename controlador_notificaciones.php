<?php
require_once 'bd.php';
require_once 'clase/clase_notificaciones.php';

function obtenerNotificaciones() {
    try {
        $conexion = obtener_conexion();
        $sql = "SELECT n.id, n.usuario_id, n.mensaje, n.fecha_creacion, n.visto, 
                       u.nombre, u.apellido, u.foto
                FROM notificaciones n
                JOIN usuarios u ON n.usuario_id = u.id
                WHERE n.visto = 0
                ORDER BY n.fecha_creacion DESC";
        
        $resultado = $conexion->query($sql);
        $notificaciones = [];
        
        while ($row = $resultado->fetch()) {
            $notificaciones[] = [
                'id' => $row['id'],
                'usuario_id' => $row['usuario_id'],
                'mensaje' => $row['mensaje'],
                'fecha_creacion' => $row['fecha_creacion'],
                'visto' => $row['visto'],
                'usuario_nombre' => $row['nombre'] . ' ' . $row['apellido'],
                'usuario_foto' => $row['foto'] ?? 'default-user.jpg'
            ];
        }
        
        return $notificaciones;
    } catch(PDOException $e) {
        error_log("Error al obtener notificaciones: " . $e->getMessage());
        return [];
    }
}

function marcarNotificacionComoVista($notificacionId) {
    try {
        $conexion = obtener_conexion();
        $sql = "UPDATE notificaciones SET visto = 1 WHERE id = :id";
        $stmt = $conexion->prepare($sql);
        return $stmt->execute(['id' => $notificacionId]);
    } catch(PDOException $e) {
        error_log("Error al marcar notificación: " . $e->getMessage());
        return false;
    }
}