-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 28, 2024 at 04:13 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `py_paginaweb`
--

-- --------------------------------------------------------

--
-- Table structure for table `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`) VALUES
(1, 'Celulares'),
(2, 'Smartwatch'),
(3, 'Accesorios'),
(4, 'Consolas'),
(5, 'Videojuegos');

-- --------------------------------------------------------

--
-- Table structure for table `detalles_pedido`
--

CREATE TABLE `detalles_pedido` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detalles_pedido`
--

INSERT INTO `detalles_pedido` (`id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 1, 3500.00),
(5, 9, 1, 3, 3500.00),
(6, 9, 3, 1, 1200.00),
(7, 9, 4, 1, 2500.00),
(8, 9, 2, 1, 2500.00),
(9, 10, 1, 1, 3500.00),
(16, 13, 5, 1, 2000.00),
(17, 14, 3, 2, 1200.00),
(18, 15, 2, 1, 2500.00),
(19, 16, 3, 1, 1200.00),
(20, 17, 2, 1, 2500.00),
(21, 18, 3, 1, 1200.00),
(22, 19, 4, 1, 2500.00),
(23, 20, 3, 1, 1200.00),
(24, 21, 2, 1, 2500.00),
(25, 22, 4, 1, 2500.00),
(27, 24, 3, 1, 1200.00),
(28, 25, 3, 1, 1200.00),
(29, 26, 3, 1, 1200.00),
(30, 27, 7, 2, 200.00),
(31, 28, 2, 1, 2300.00),
(32, 28, 3, 1, 1200.00),
(33, 28, 4, 1, 2500.00),
(34, 29, 3, 1, 1200.00),
(35, 29, 2, 1, 2300.00),
(36, 29, 3, 1, 1200.00),
(37, 29, 4, 1, 2500.00),
(38, 30, 2, 1, 2300.00),
(39, 30, 3, 1, 1200.00),
(40, 30, 4, 1, 2500.00),
(41, 31, 1, 1, 3000.00),
(42, 31, 3, 1, 1200.00),
(43, 31, 4, 1, 2500.00),
(44, 32, 5, 16, 2000.00),
(45, 33, 2, 1, 2300.00),
(46, 33, 3, 1, 1200.00),
(47, 33, 4, 1, 2500.00),
(48, 34, 2, 1, 2300.00),
(49, 34, 3, 1, 1200.00),
(50, 34, 4, 1, 2500.00),
(51, 35, 2, 1, 2300.00),
(52, 35, 3, 1, 1200.00),
(53, 35, 4, 1, 2500.00),
(54, 36, 2, 1, 2300.00),
(55, 36, 3, 1, 1200.00),
(56, 36, 4, 1, 2500.00),
(57, 36, 2, 1, 2300.00),
(58, 36, 3, 1, 1200.00),
(59, 36, 4, 1, 2500.00),
(60, 37, 10, 1, 800.99),
(61, 38, 5, 1, 2000.00),
(62, 38, 6, 1, 200.00),
(63, 39, 11, 2, 100.00),
(64, 40, 3, 1, 1200.00),
(65, 41, 3, 1, 1200.00),
(66, 42, 3, 1, 1200.00),
(67, 43, 1, 1, 3000.00),
(68, 43, 3, 1, 1200.00),
(69, 43, 4, 1, 2500.00);

-- --------------------------------------------------------

--
-- Table structure for table `direcciones`
--

CREATE TABLE `direcciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `direcciones`
--

INSERT INTO `direcciones` (`id`, `usuario_id`, `direccion`, `ciudad`, `estado`, `pais`, `codigo_postal`) VALUES
(1, 1, 'Av. Elvira Garcia y Garcia 455as', 'Chiclayoa', 'Lambayequea', 'aPeru', '140117'),
(7, 3, '355 East Primm Boulevard', 'Jean', 'NV', 'United States', '89019'),
(12, 3, 'Av. Elvira Garcia y Garcia 455', 'Chiclayo', 'Lambayeque', 'Peru', '14011'),
(13, 3, 'Av. Argentina', 'Lima', 'MIraflores', 'Perú', '14000'),
(14, 1, '355 East Primm Boulevards', 'janaja', 'NVs', 'United Statess', '89019s');

-- --------------------------------------------------------

--
-- Table structure for table `favoritos`
--

CREATE TABLE `favoritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `favoritos`
--

INSERT INTO `favoritos` (`id`, `usuario_id`, `producto_id`) VALUES
(7, 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `kits`
--

CREATE TABLE `kits` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `celular_id` int(11) DEFAULT NULL,
  `smartwatch_id` int(11) DEFAULT NULL,
  `accesorios_id` int(11) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kits`
--

INSERT INTO `kits` (`id`, `usuario_id`, `celular_id`, `smartwatch_id`, `accesorios_id`, `fecha_creacion`) VALUES
(4, 1, 1, 3, 4, '2024-10-17 02:06:12'),
(5, 1, 1, 3, 4, '2024-10-17 04:02:13');

-- --------------------------------------------------------

--
-- Table structure for table `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `pedido_id` int(11) DEFAULT NULL,
  `mensaje` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `visto` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `pedido_id`, `mensaje`, `fecha_creacion`, `visto`) VALUES
(1, 3, 19, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 2500.00', '2024-10-23 01:24:35', 1),
(18, 1, 42, 'El usuario \"Roger\" acaba de realizar una compra por S/. 1200.00', '2024-10-25 21:34:37', 0),
(19, 1, 43, 'El usuario \"Roger\" acaba de realizar una compra por S/. 6700.00', '2024-10-26 00:18:01', 0);

-- --------------------------------------------------------

--
-- Table structure for table `opiniones`
--

CREATE TABLE `opiniones` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `comentario` text DEFAULT NULL,
  `calificacion` int(11) DEFAULT NULL CHECK (`calificacion` between 1 and 5),
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `opiniones`
--

INSERT INTO `opiniones` (`id`, `producto_id`, `usuario_id`, `comentario`, `calificacion`, `fecha`) VALUES
(3, 3, 1, 'Este producto esta muy bien :)', 3, '2024-10-23 23:32:40'),
(4, 3, 3, 'Bueno', 1, '2024-10-24 00:53:03'),
(5, 1, 1, 'Bueno', 3, '2024-10-24 01:06:47'),
(6, 3, 1, 'Me gusto mas de lo que esperaba', 2, '2024-10-24 23:08:19'),
(7, 3, 1, 'EL MEJOR PRODUCTO DE TODOS', 5, '2024-10-24 23:08:35'),
(8, 11, 1, 'El GOTY', 5, '2024-10-26 00:35:27');

-- --------------------------------------------------------

--
-- Table structure for table `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `direccion_id` int(11) NOT NULL,
  `fecha_pedido` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pedidos`
--

INSERT INTO `pedidos` (`id`, `usuario_id`, `direccion_id`, `fecha_pedido`, `estado`) VALUES
(1, 1, 1, '2024-10-16 22:03:32', 'pendiente'),
(5, 1, 1, '2024-10-16 22:13:08', 'pendiente'),
(6, 1, 1, '2024-10-16 22:14:20', 'pendiente'),
(7, 1, 1, '2024-10-16 22:15:36', 'pendiente'),
(8, 1, 1, '2024-10-16 22:15:52', 'pendiente'),
(9, 1, 1, '2024-10-16 22:49:19', 'pendiente'),
(10, 1, 1, '2024-10-16 23:10:06', 'pendiente'),
(13, 1, 1, '2024-10-18 20:04:12', 'pendiente'),
(14, 1, 1, '2024-10-22 19:01:55', 'pendiente'),
(15, 1, 1, '2024-10-22 19:06:06', 'pendiente'),
(16, 1, 1, '2024-10-22 19:06:33', 'pendiente'),
(17, 1, 1, '2024-10-22 19:08:41', 'pendiente'),
(18, 1, 1, '2024-10-22 20:11:36', 'pendiente'),
(19, 3, 12, '2024-10-22 20:24:35', 'pendiente'),
(20, 3, 12, '2024-10-22 20:26:18', 'pendiente'),
(21, 3, 7, '2024-10-22 00:00:00', 'NV'),
(22, 3, 13, '2024-10-22 00:00:00', 'Ferrañafe'),
(24, 1, 1, '2024-10-22 00:00:00', 'Lambayeque'),
(25, 1, 1, '2024-10-23 18:26:58', 'pendiente'),
(26, 1, 14, '2024-10-23 18:32:55', 'pendiente'),
(27, 1, 1, '2024-10-23 00:00:00', 'Lambayequea'),
(28, 1, 14, '2024-10-23 19:49:11', 'pendiente'),
(29, 3, 13, '2024-10-23 19:54:04', 'pendiente'),
(30, 3, 7, '2024-10-23 19:55:10', 'pendiente'),
(31, 3, 13, '2024-10-23 00:00:00', 'MIraflores'),
(32, 1, 14, '2024-10-23 20:08:51', 'pendiente'),
(33, 1, 1, '2024-10-23 20:09:50', 'pendiente'),
(34, 1, 1, '2024-10-23 20:09:53', 'pendiente'),
(35, 1, 1, '2024-10-23 20:09:58', 'pendiente'),
(36, 1, 1, '2024-10-23 20:12:29', 'pendiente'),
(37, 1, 1, '2024-10-23 20:15:54', 'pendiente'),
(38, 1, 14, '2024-10-23 20:20:32', 'pendiente'),
(39, 1, 1, '2024-10-23 20:33:02', 'pendiente'),
(40, 1, 1, '2024-10-24 18:00:45', 'pendiente'),
(41, 1, 1, '2024-10-25 16:30:14', 'pendiente'),
(42, 1, 14, '2024-10-25 16:34:37', 'pendiente'),
(43, 1, 14, '2024-10-25 19:18:01', 'pendiente');

-- --------------------------------------------------------

--
-- Table structure for table `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `categoria_id` int(11) DEFAULT NULL,
  `destacado` tinyint(1) DEFAULT 0,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `categoria_id`, `destacado`, `imagen`) VALUES
(1, 'Iphone 15', 'Descubre la innovación con el iPhone 15, un dispositivo diseñado para redefinir tus expectativas. Con una pantalla Super Retina XDR más brillante y tecnología Dynamic Island, cada interacción se vuelve más intuitiva. Equipado con el potente chip A16 Bionic, asegura un rendimiento ultrarrápido y eficiencia energética. Su cámara de 48 MP eleva la fotografía móvil al siguiente nivel, permitiendo capturar cada momento con una nitidez impresionante. Además, la integración de USB-C facilita la conectividad universal. El iPhone 15 combina diseño elegante y tecnología de vanguardia, listo para acompañarte en cada aventura.', 3000.00, 29, 1, 0, 'Iphone_15.png'),
(2, 'Iphone 12', 'El iPhone 12 sigue destacando como un clásico moderno, ofreciendo la combinación perfecta entre estilo y rendimiento. Con una pantalla OLED Super Retina XDR y el poderoso chip A14 Bionic, brinda una experiencia fluida para multitareas y juegos. Su sistema de cámara dual captura fotos vibrantes y vídeos en 4K, mientras que su diseño con bordes planos aporta elegancia y durabilidad. Compatible con 5G y con carga rápida MagSafe, el iPhone 12 es una opción sólida para los amantes de la tecnología que buscan calidad y eficiencia en un solo dispositivo.', 2300.00, 20, 1, 0, 'Iphone_12.png'),
(3, 'Apple Watch SE', 'El Apple Watch SE combina las mejores funciones esenciales del Apple Watch con un diseño moderno y accesible. Perfecto para llevar un estilo de vida activo, ofrece seguimiento avanzado de actividad física, notificaciones de frecuencia cardíaca y detección de caídas. Su integración con watchOS permite acceder a aplicaciones, responder mensajes y controlar tu música desde la muñeca. Compatible con Apple Fitness+, este reloj inteligente se convierte en tu aliado ideal para alcanzar metas de salud y bienestar. Además, su diseño ligero y personalizable con correas intercambiables lo convierte en el complemento perfecto para cualquier ocasión.', 1200.00, 20, 2, 0, 'applewatch_se.jpg'),
(4, 'Airpods Max', 'Sumérgete en una experiencia de sonido única con los AirPods Max. Diseñados con una combinación perfecta de lujo y tecnología, estos audífonos inalámbricos ofrecen un audio envolvente con cancelación activa de ruido y modo de sonido ambiente para mantenerte conectado con tu entorno cuando lo necesites. Equipados con controladores dinámicos diseñados por Apple, brindan una calidad de sonido excepcional con graves profundos y agudos cristalinos. Su diadema de malla transpirable y almohadillas de espuma viscoelástica garantizan comodidad durante horas de uso. Con Audio Espacial y compatibilidad con Siri, los AirPods Max son la opción perfecta para quienes buscan disfrutar de la música y el entretenimiento sin compromisos.', 2500.00, 17, 3, 0, 'airpods_max.jpg'),
(5, 'PS5 Slim', 'Vive la próxima generación de videojuegos con la PS5 Slim, la versión más compacta y elegante de la consola insignia de Sony. Manteniendo el poder del hardware original, esta consola ofrece gráficos impresionantes en 4K HDR, tiempos de carga ultrarrápidos gracias al SSD de alta velocidad, y compatibilidad con ray tracing para una inmersión visual sin precedentes. Su diseño más delgado y ligero se adapta perfectamente a cualquier espacio. Además, con acceso a juegos exclusivos de PlayStation y el servicio PS Plus, la PS5 Slim es ideal para quienes buscan potencia y estilo en una consola de nueva generación.', 2000.00, 19, 4, 0, 'ps5_slim.jpg'),
(6, 'God of War Ragnarok', 'Embárcate en una épica aventura con God of War: Ragnarök, la esperada secuela que sigue la historia de Kratos y su hijo Atreus mientras enfrentan el fin de los tiempos en la mitología nórdica. Con un impresionante mundo abierto, gráficos mejorados en 4K y combates más fluidos, este título ofrece una experiencia inmersiva llena de desafíos y momentos inolvidables. Explora los nueve reinos y enfréntate a nuevos dioses y criaturas míticas mientras Kratos lidia con su destino como guerrero y padre. La jugabilidad combina acción intensa, resolución de acertijos y un profundo desarrollo narrativo que te atrapará desde el primer momento.\r\n\r\nPrepárate para desafiar el destino y enfrentar a los dioses en esta emocionante obra maestra exclusiva de PlayStation.', 200.00, 49, 5, 0, 'god_of_war_ragnarok.jpg'),
(7, 'Crash Twinsanity', 'videojuego antiguos', 200.00, 98, 5, 0, 'crash.jpg'),
(10, 'Iphone XR', 'un celular', 800.99, 20, 1, 0, 'iphone_xr.jpg'),
(11, 'GTA V', 'Videojuego', 100.00, 0, 5, 0, 'gtav.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `tipo` enum('cliente','administrador') DEFAULT 'cliente',
  `foto` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `contraseña`, `tipo`, `foto`, `fecha_registro`) VALUES
(1, 'Roger', 'Zavaleta', 'meencantas7u7@gmail.com', '$2b$12$SYr0n45Sj9X4fM1zzIYUZO9SJtAq7XNATT.BUxrKWEro4qmtAWtoG', 'administrador', 'cliente2.jpg', '2024-10-17 00:46:55'),
(3, 'Abraham', 'Vidaurre', 'cliente@gmail.com', '$2b$12$NSXzq1c8RksnOj6pk6pCYer4Z88Eno93fCTcMrWfG.VSKJ/qBfR1m', 'cliente', NULL, '2024-10-18 18:16:52');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indexes for table `direcciones`
--
ALTER TABLE `direcciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indexes for table `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indexes for table `kits`
--
ALTER TABLE `kits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `celular_id` (`celular_id`),
  ADD KEY `funda_id` (`smartwatch_id`),
  ADD KEY `audifonos_id` (`accesorios_id`);

--
-- Indexes for table `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `pedido_id` (`pedido_id`);

--
-- Indexes for table `opiniones`
--
ALTER TABLE `opiniones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indexes for table `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `direccion_id` (`direccion_id`);

--
-- Indexes for table `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `categoria_id` (`categoria_id`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `direcciones`
--
ALTER TABLE `direcciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `kits`
--
ALTER TABLE `kits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `opiniones`
--
ALTER TABLE `opiniones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD CONSTRAINT `detalles_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  ADD CONSTRAINT `detalles_pedido_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Constraints for table `direcciones`
--
ALTER TABLE `direcciones`
  ADD CONSTRAINT `direcciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Constraints for table `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Constraints for table `kits`
--
ALTER TABLE `kits`
  ADD CONSTRAINT `kits_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `kits_ibfk_2` FOREIGN KEY (`celular_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `kits_ibfk_3` FOREIGN KEY (`smartwatch_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `kits_ibfk_4` FOREIGN KEY (`accesorios_id`) REFERENCES `productos` (`id`);

--
-- Constraints for table `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `notificaciones_ibfk_2` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`);

--
-- Constraints for table `opiniones`
--
ALTER TABLE `opiniones`
  ADD CONSTRAINT `opiniones_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `opiniones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Constraints for table `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`direccion_id`) REFERENCES `direcciones` (`id`);

--
-- Constraints for table `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
