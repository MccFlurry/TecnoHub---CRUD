-- Tabla Pais: Almacena los países
CREATE TABLE Pais (
    idPais INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla Marca: Almacena las marcas de los productos
CREATE TABLE Marca (
    idMarca INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla Modelo: Almacena los modelos de los productos
CREATE TABLE Modelo (
    idModelo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- Tabla Categoria: Almacena las categorías de productos
CREATE TABLE Categoria (
    idCategoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Tabla Usuario: Tabla principal para clientes y trabajadores
CREATE TABLE Usuario (
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,        -- Encriptada
    telefono_contacto VARCHAR(20),
    tipo_usuario VARCHAR(20) NOT NULL,       -- Tipo de usuario ('cliente' o 'trabajador')
    fecha_registro DATE DEFAULT CURRENT_DATE,
    CONSTRAINT chk_tipo_usuario CHECK (tipo_usuario IN ('cliente', 'trabajador'))
) ENGINE=InnoDB;

-- Tabla Cliente: Relación uno a uno con Usuario, información específica del cliente
CREATE TABLE Cliente (
    idCliente INT PRIMARY KEY AUTO_INCREMENT,
    idUsuario INT UNIQUE,
    fecha_nacimiento DATE,
    tipo_documento VARCHAR(50),
    numero_documento VARCHAR(50),
    idPais INT,
    CONSTRAINT fk_usuario_cliente FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_pais_cliente FOREIGN KEY (idPais) REFERENCES Pais(idPais)
) ENGINE=InnoDB;

-- Tabla Trabajador: Relación uno a uno con Usuario, información específica del trabajador
CREATE TABLE Trabajador (
    idTrabajador INT PRIMARY KEY AUTO_INCREMENT,
    idUsuario INT UNIQUE,
    numero_documento VARCHAR(50),
    tipo_documento VARCHAR(20),
    fecha_nacimiento DATE,
    fecha_ingreso DATE,
    sexo CHAR(1),
    cargo VARCHAR(50) NOT NULL DEFAULT 'Administrador',  -- Solo permite el valor 'Administrador' por el momento
    vigencia TINYINT(1) DEFAULT 1,         -- Vigencia (1 = activo, 0 = inactivo)
    idPais INT,
    CONSTRAINT fk_usuario_trabajador FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_pais_trabajador FOREIGN KEY (idPais) REFERENCES Pais(idPais)
) ENGINE=InnoDB;

-- Tabla Division_Geografica: Almacena las divisiones administrativas (departamentos, regiones, etc.)
CREATE TABLE Division_Geografica (
    idDivision INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    nivel INT,  -- Nivel de la división (1 = departamento, 2 = provincia, etc.)
    idPais INT,
    CONSTRAINT fk_pais_division FOREIGN KEY (idPais) REFERENCES Pais(idPais)
) ENGINE=InnoDB;

-- Tabla Ubicacion: Almacena las ubicaciones específicas (ciudades, distritos, etc.)
CREATE TABLE Ubicacion (
    idUbicacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    idDivision INT,
    CONSTRAINT fk_division_ubicacion FOREIGN KEY (idDivision) REFERENCES Division_Geografica(idDivision)
) ENGINE=InnoDB;

-- Tabla DireccionEnvio: Relaciona usuarios con una o más direcciones de envío
CREATE TABLE DireccionEnvio (
    idDireccion INT PRIMARY KEY AUTO_INCREMENT,
    idUsuario INT,
    direccion VARCHAR(255) NOT NULL,
    codigoPostal VARCHAR(20),
    referencia VARCHAR(255),
    idPais INT,
    idDivision1 INT,
    idDivision2 INT,
    idDivision3 INT,
    CONSTRAINT fk_usuario_direccion FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_pais_direccion FOREIGN KEY (idPais) REFERENCES Pais(idPais),
    CONSTRAINT fk_division1_direccion FOREIGN KEY (idDivision1) REFERENCES Division_Geografica(idDivision),
    CONSTRAINT fk_division2_direccion FOREIGN KEY (idDivision2) REFERENCES Division_Geografica(idDivision),
    CONSTRAINT fk_division3_direccion FOREIGN KEY (idDivision3) REFERENCES Division_Geografica(idDivision)
) ENGINE=InnoDB;

-- Tabla Producto: Almacena información sobre los productos disponibles
CREATE TABLE Producto (
    idProducto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    stock INT,
    precio DECIMAL(9, 2),
    color VARCHAR(50),
    idMarca INT,
    idModelo INT,
    idCategoria INT,
    CONSTRAINT fk_marca_producto FOREIGN KEY (idMarca) REFERENCES Marca(idMarca),
    CONSTRAINT fk_modelo_producto FOREIGN KEY (idModelo) REFERENCES Modelo(idModelo),
    CONSTRAINT fk_categoria_producto FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria)
) ENGINE=InnoDB;

-- Tabla Kit: Permite a los usuarios armar un kit de productos
CREATE TABLE Kit (
    idKit INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    idUsuario INT,
    CONSTRAINT fk_usuario_kit FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
) ENGINE=InnoDB;

-- Tabla Detalle_Kit: Detalle de los productos dentro de un kit
CREATE TABLE Detalle_Kit (
    id_kit_detalle INT PRIMARY KEY AUTO_INCREMENT,
    idKit INT,
    idCategoria INT,
    idProducto INT,
    CONSTRAINT fk_kit_detalle FOREIGN KEY (idKit) REFERENCES Kit(idKit),
    CONSTRAINT fk_categoria_detalle FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria),
    CONSTRAINT fk_producto_detalle FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
) ENGINE=InnoDB;

-- Tabla Calificacion: Permite a los usuarios calificar productos
CREATE TABLE Calificacion (
    idCalificacion INT PRIMARY KEY AUTO_INCREMENT,
    puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
    opinion VARCHAR(200),
    fecha DATE,
    hora TIME,
    idUsuario INT,
    idProducto INT,
    CONSTRAINT fk_usuario_calificacion FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_producto_calificacion FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
) ENGINE=InnoDB;

-- Tabla Transaccion: Almacena las transacciones realizadas por los usuarios
CREATE TABLE Transaccion (
    idTransaccion INT PRIMARY KEY AUTO_INCREMENT,
    tipoTransaccion VARCHAR(100),
    cantidad INT,
    estado CHAR(1),
    metodo_pago VARCHAR(100),
    total DECIMAL(9, 2),
    subTotal DECIMAL(9, 2),
    fechaTransaccion DATE,
    horaTransaccion TIME,
    idUsuario INT,
    idDireccion INT,
    CONSTRAINT fk_usuario_transaccion FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_direccion_transaccion FOREIGN KEY (idDireccion) REFERENCES DireccionEnvio(idDireccion)
) ENGINE=InnoDB;

-- Tabla Detalle_Transaccion: Almacena los productos comprados en una transacción
CREATE TABLE Detalle_Transaccion (
    idDetalleTransaccion INT PRIMARY KEY AUTO_INCREMENT,
    idTransaccion INT,
    idProducto INT,
    cantidad INT,
    precio_unitario DECIMAL(9, 2),
    CONSTRAINT fk_transaccion_detalle FOREIGN KEY (idTransaccion) REFERENCES Transaccion(idTransaccion),
    CONSTRAINT fk_producto_transaccion FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
) ENGINE=InnoDB;

-- Tabla Comprobante: Almacena los comprobantes generados tras una transacción
CREATE TABLE Comprobante (
    idComprobante INT PRIMARY KEY AUTO_INCREMENT,
    tipoComprobante VARCHAR(30),
    fecha DATE,
    hora TIME,
    isna VARCHAR(100) UNIQUE,
    total DECIMAL(9, 2),
    subTotal DECIMAL(9, 2),
    idUsuario INT,
    idTransaccion INT,
    CONSTRAINT fk_usuario_comprobante FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario),
    CONSTRAINT fk_transaccion_comprobante FOREIGN KEY (idTransaccion) REFERENCES Transaccion(idTransaccion)
) ENGINE=InnoDB;

-- Tabla Detalle_Comprobante: Detalle de los productos en el comprobante
CREATE TABLE Detalle_Comprobante (
    idDetalleComprobante INT PRIMARY KEY AUTO_INCREMENT,
    idComprobante INT,
    idProducto INT,
    precio_unitario DECIMAL(9, 2),
    monto DECIMAL(9, 2),
    cantidad INT,
    CONSTRAINT fk_comprobante_detalle FOREIGN KEY (idComprobante) REFERENCES Comprobante(idComprobante),
    CONSTRAINT fk_producto_comprobante FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
) ENGINE=InnoDB;