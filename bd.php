<?php
function obtener_conexion() {
    $host = "127.0.0.1";
    $dbname = "py_paginaweb";
    $usuario = "root";
    $password = "";  // XAMPP usa password vacío por defecto
    
    try {
        $opciones = array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        );

        // Puerto 3306 es el que usa XAMPP por defecto
        $dsn = "mysql:host=$host;port=3306;dbname=$dbname;charset=utf8mb4";
        $conexion = new PDO($dsn, $usuario, $password, $opciones);
        
        return $conexion;
    } catch (PDOException $e) {
        error_log("Error de conexión: " . $e->getMessage());
        die("Error al conectar con la base de datos. Por favor, intente más tarde.");
    }
}