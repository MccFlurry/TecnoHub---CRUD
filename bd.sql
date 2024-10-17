-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS py_paginaweb;
USE py_paginaweb;

-- Tabla de categorías (no tiene dependencias)
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla de usuarios (no tiene dependencias)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    tipo ENUM('cliente', 'administrador') DEFAULT 'cliente',
    foto VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    categoria_id INT,
    destacado TINYINT(1) DEFAULT 0,
    imagen VARCHAR(255),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla de direcciones (depende de usuarios)
CREATE TABLE direcciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    direccion TEXT,
    ciudad VARCHAR(100),
    estado VARCHAR(100),
    pais VARCHAR(100),
    codigo_postal VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de pedidos (depende de usuarios y direcciones)
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    direccion_id INT NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (direccion_id) REFERENCES direcciones(id)
);

-- Tabla de detalles de pedido (depende de pedidos y productos)
CREATE TABLE detalles_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de opiniones (depende de productos y usuarios)
CREATE TABLE opiniones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    usuario_id INT,
    comentario TEXT,
    calificacion INT CHECK (calificacion BETWEEN 1 AND 5),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de favoritos (depende de productos y usuarios)
CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    producto_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla para "Arma tu kit" (depende de productos y usuarios)
CREATE TABLE kits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    celular_id INT,
    smartwatch_id INT,
    accesorios_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (celular_id) REFERENCES productos(id),
    FOREIGN KEY (smartwatch_id) REFERENCES productos(id),
    FOREIGN KEY (accesorios_id) REFERENCES productos(id)
);

-- Tabla para productos visitados recientemente (depende de productos y usuarios)
CREATE TABLE productos_visitados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    producto_id INT,
    fecha_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
