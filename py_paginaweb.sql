-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 23-11-2024 a las 22:24:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `py_paginaweb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `fecha_creacion`) VALUES
(1, 'Celulares', '2024-11-23 19:19:53'),
(2, 'Smartwatch', '2024-11-23 19:19:53'),
(3, 'Accesorios', '2024-11-23 19:19:53'),
(4, 'Consolas', '2024-11-23 19:19:53'),
(5, 'Videojuegos', '2024-11-23 19:19:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciudades`
--

CREATE TABLE `ciudades` (
  `id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo_postal_patron` varchar(20) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_modificacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `ciudades`
--

INSERT INTO `ciudades` (`id`, `estado_id`, `nombre`, `codigo_postal_patron`, `activo`, `fecha_creacion`, `fecha_modificacion`) VALUES
(1, 1, 'Lima', '15001', 1, '2024-11-15 21:08:54', '2024-11-15 21:08:54'),
(2, 2, 'Chiclayo', '14001', 1, '2024-11-15 21:08:54', '2024-11-15 21:08:54'),
(4, 4, 'La Plata', '1900', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(5, 4, 'Mar del Plata', '7600', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(6, 4, 'Quilmes', '1878', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(7, 7, 'São Paulo', '01000-000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(8, 7, 'Campinas', '13000-000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(9, 7, 'Santos', '11000-000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(10, 10, 'Santiago', '8320000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(11, 10, 'Maipú', '9250000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(12, 10, 'Las Condes', '7550000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(13, 13, 'Cuauhtémoc', '06000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(14, 13, 'Miguel Hidalgo', '11000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(15, 13, 'Benito Juárez', '03000', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_pedido`
--

CREATE TABLE `detalles_pedido` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_pedido`
--

INSERT INTO `detalles_pedido` (`id`, `pedido_id`, `producto_id`, `cantidad`, `precio_unitario`, `fecha_creacion`) VALUES
(1, 1, 1, 1, 3500.00, '2024-11-23 19:19:53'),
(5, 9, 1, 3, 3500.00, '2024-11-23 19:19:53'),
(6, 9, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(7, 9, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(8, 9, 2, 1, 2500.00, '2024-11-23 19:19:53'),
(9, 10, 1, 1, 3500.00, '2024-11-23 19:19:53'),
(16, 13, 5, 1, 2000.00, '2024-11-23 19:19:53'),
(17, 14, 3, 2, 1200.00, '2024-11-23 19:19:53'),
(18, 15, 2, 1, 2500.00, '2024-11-23 19:19:53'),
(19, 16, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(20, 17, 2, 1, 2500.00, '2024-11-23 19:19:53'),
(21, 18, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(22, 19, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(23, 20, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(24, 21, 2, 1, 2500.00, '2024-11-23 19:19:53'),
(25, 22, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(27, 24, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(28, 25, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(29, 26, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(30, 27, 7, 2, 200.00, '2024-11-23 19:19:53'),
(31, 28, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(32, 28, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(33, 28, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(34, 29, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(35, 29, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(36, 29, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(37, 29, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(38, 30, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(39, 30, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(40, 30, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(41, 31, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(42, 31, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(43, 31, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(44, 32, 5, 16, 2000.00, '2024-11-23 19:19:53'),
(45, 33, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(46, 33, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(47, 33, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(48, 34, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(49, 34, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(50, 34, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(51, 35, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(52, 35, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(53, 35, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(54, 36, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(55, 36, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(56, 36, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(57, 36, 2, 1, 2300.00, '2024-11-23 19:19:53'),
(58, 36, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(59, 36, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(60, 37, 10, 1, 800.99, '2024-11-23 19:19:53'),
(61, 38, 5, 1, 2000.00, '2024-11-23 19:19:53'),
(62, 38, 6, 1, 200.00, '2024-11-23 19:19:53'),
(63, 39, 11, 2, 100.00, '2024-11-23 19:19:53'),
(64, 40, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(65, 41, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(66, 42, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(67, 43, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(68, 43, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(69, 43, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(70, 44, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(71, 45, 7, 1, 200.00, '2024-11-23 19:19:53'),
(72, 46, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(73, 47, 6, 1, 200.00, '2024-11-23 19:19:53'),
(74, 48, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(75, 49, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(76, 50, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(77, 51, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(78, 52, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(79, 53, 11, 1, 100.00, '2024-11-23 19:19:53'),
(80, 54, 10, 1, 800.99, '2024-11-23 19:19:53'),
(81, 55, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(82, 56, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(83, 57, 5, 1, 2000.00, '2024-11-23 19:19:53'),
(84, 58, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(85, 59, 1, 1, 3000.00, '2024-11-23 19:19:53'),
(86, 59, 3, 1, 1200.00, '2024-11-23 19:19:53'),
(87, 59, 4, 1, 2500.00, '2024-11-23 19:19:53'),
(88, 60, 11, 3, 100.00, '2024-11-23 19:42:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direcciones`
--

CREATE TABLE `direcciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(20) DEFAULT NULL,
  `distrito_id` int(11) DEFAULT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  `direccion_completa` text DEFAULT NULL,
  `numero` varchar(20) DEFAULT NULL,
  `departamento` varchar(50) DEFAULT NULL,
  `direccion_predeterminada` tinyint(1) DEFAULT 0,
  `cached_ubicacion_id` int(11) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `direcciones`
--

INSERT INTO `direcciones` (`id`, `usuario_id`, `direccion`, `ciudad`, `estado`, `pais`, `codigo_postal`, `distrito_id`, `latitud`, `longitud`, `direccion_completa`, `numero`, `departamento`, `direccion_predeterminada`, `cached_ubicacion_id`, `fecha_creacion`) VALUES
(1, 1, 'Av. Elvira Garcia y Garcia 455', 'Lima', 'Lima', 'Perú', '140117', 1, NULL, NULL, 'Av. Elvira Garcia y Garcia 455, Miraflores, Lima, Lima, Perú', NULL, NULL, 1, NULL, '2024-11-23 19:21:42'),
(7, 3, '355 East Primm Boulevard', 'Jean', 'NV', 'United States', '89019', NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, '2024-11-23 19:21:42'),
(12, 3, 'Av. Elvira Garcia y Garcia 455', 'Chiclayo', 'Lambayeque', 'Perú', '14011', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, '2024-11-23 19:21:42'),
(13, 3, 'Av. Argentina', 'Lima', 'MIraflores', 'Perú', '14000', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, '2024-11-23 19:21:42'),
(14, 1, 'Av Gran Chimu 1624', 'Benito Juárez', 'Ciudad de México', 'México', '13012', NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, '2024-11-23 19:21:42');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distritos`
--

CREATE TABLE `distritos` (
  `id` int(11) NOT NULL,
  `ciudad_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_modificacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `distritos`
--

INSERT INTO `distritos` (`id`, `ciudad_id`, `nombre`, `activo`, `fecha_creacion`, `fecha_modificacion`) VALUES
(1, 1, 'Miraflores', 1, '2024-11-15 21:08:55', '2024-11-15 21:08:55'),
(2, 1, 'San Isidro', 1, '2024-11-15 21:08:55', '2024-11-15 21:08:55'),
(3, 2, 'Chiclayo', 1, '2024-11-15 21:08:55', '2024-11-15 21:08:55'),
(4, 4, 'Centro', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(5, 4, 'Tolosa', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(6, 4, 'Los Hornos', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(7, 7, 'Moema', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(8, 7, 'Pinheiros', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(9, 7, 'Vila Mariana', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(10, 10, 'Santiago Centro', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(11, 10, 'Providencia', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(12, 10, 'Ñuñoa', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(13, 13, 'Centro Histórico', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(14, 13, 'Roma Norte', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(15, 13, 'Condesa', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados`
--

CREATE TABLE `estados` (
  `id` int(11) NOT NULL,
  `pais_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo` varchar(10) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_modificacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `estados`
--

INSERT INTO `estados` (`id`, `pais_id`, `nombre`, `codigo`, `activo`, `fecha_creacion`, `fecha_modificacion`) VALUES
(1, 1, 'Lima', 'LIM', 1, '2024-11-15 21:08:54', '2024-11-15 21:08:54'),
(2, 1, 'Lambayeque', 'LAM', 1, '2024-11-15 21:08:54', '2024-11-15 21:08:54'),
(4, 10, 'Buenos Aires', 'BA', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(5, 10, 'Córdoba', 'CB', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(6, 10, 'Santa Fe', 'SF', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(7, 11, 'São Paulo', 'SP', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(8, 11, 'Rio de Janeiro', 'RJ', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(9, 11, 'Minas Gerais', 'MG', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(10, 12, 'Región Metropolitana', 'RM', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(11, 12, 'Valparaíso', 'VA', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(12, 12, 'Biobío', 'BB', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(13, 14, 'Ciudad de México', 'CDMX', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(14, 14, 'Jalisco', 'JAL', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(15, 14, 'Nuevo León', 'NL', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `favoritos`
--

INSERT INTO `favoritos` (`id`, `usuario_id`, `producto_id`, `fecha_creacion`) VALUES
(15, 3, 4, '2024-11-23 19:35:51');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `geocoding_cache`
--

CREATE TABLE `geocoding_cache` (
  `id` int(11) NOT NULL,
  `direccion_completa` text NOT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  `datos_api` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_api`)),
  `fecha_consulta` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_expiracion` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `kits`
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
-- Volcado de datos para la tabla `kits`
--

INSERT INTO `kits` (`id`, `usuario_id`, `celular_id`, `smartwatch_id`, `accesorios_id`, `fecha_creacion`) VALUES
(4, 1, 1, 3, 4, '2024-10-17 02:06:12'),
(5, 1, 1, 3, 4, '2024-10-17 04:02:13');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marcas`
--

CREATE TABLE `marcas` (
  `id` int(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marcas`
--

INSERT INTO `marcas` (`id`, `nombre`, `fecha_creacion`) VALUES
(1, 'Apple', '2024-11-23 19:19:53'),
(2, 'Samsung', '2024-11-23 19:19:53'),
(3, 'Sony', '2024-11-23 19:19:53'),
(4, 'Microsoft', '2024-11-23 19:19:53'),
(5, 'Nintendo', '2024-11-23 19:19:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodos_pago`
--

CREATE TABLE `metodos_pago` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `numero_tarjeta` varchar(255) NOT NULL,
  `titular` varchar(100) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `cvv` varchar(255) NOT NULL,
  `predeterminado` tinyint(1) DEFAULT 0,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `metodos_pago`
--

INSERT INTO `metodos_pago` (`id`, `usuario_id`, `tipo`, `numero_tarjeta`, `titular`, `fecha_vencimiento`, `cvv`, `predeterminado`, `fecha_registro`, `activo`) VALUES
(1, 1, 'mastercard', '1231241241414144', 'Roger Zavaleta', '2029-06-01', '$2b$12$dAfPROgACCcIne25jGCB1eDZW4z0FOoJN.Qsl2hCZRQjg7Zrf9vYO', 1, '2024-11-16 19:29:23', 1),
(2, 3, 'visa', '1111111111111111', 'Abraham Viduarre', '2028-11-01', '$2b$12$i7uzRtZo2DP2ZNn971e5MOksI4Rjtl.3DLnye3mW63TED5FxVEwN6', 1, '2024-11-23 19:42:09', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelos`
--

CREATE TABLE `modelos` (
  `id` int(10) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `modelos`
--

INSERT INTO `modelos` (`id`, `nombre`, `fecha_creacion`) VALUES
(1, 'iPhone 15', '2024-11-23 19:19:53'),
(2, 'iPhone 12', '2024-11-23 19:19:53'),
(3, 'Apple Watch SE', '2024-11-23 19:19:53'),
(4, 'AirPods Max', '2024-11-23 19:19:53'),
(5, 'PlayStation 5 Slim', '2024-11-23 19:19:53'),
(6, 'Xbox Series X', '2024-11-23 19:19:53'),
(7, 'Nintendo Switch', '2024-11-23 19:19:53'),
(8, 'Galaxy S23', '2024-11-23 19:19:53'),
(9, 'Galaxy Watch 6', '2024-11-23 19:19:53'),
(10, 'WH-1000XM4', '2024-11-23 19:19:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
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
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `pedido_id`, `mensaje`, `fecha_creacion`, `visto`) VALUES
(1, 3, 19, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 2500.00', '2024-10-23 01:24:35', 1),
(18, 1, 42, 'El usuario \"Roger\" acaba de realizar una compra por S/. 1200.00', '2024-10-25 21:34:37', 1),
(19, 1, 43, 'El usuario \"Roger\" acaba de realizar una compra por S/. 6700.00', '2024-10-26 00:18:01', 1),
(20, 1, 44, 'El usuario \"Roger\" acaba de realizar una compra por S/. 1200.00', '2024-11-08 04:06:47', 0),
(21, 3, 45, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 200.00', '2024-11-08 22:47:31', 0),
(22, 1, 46, 'El usuario \"Roger\" acaba de realizar una compra por S/. 2500.00', '2024-11-08 22:52:53', 1),
(23, 1, 47, 'El usuario \"Roger\" acaba de realizar una compra por S/. 200.00', '2024-11-09 00:15:50', 1),
(24, 1, 48, 'El usuario \"Roger\" acaba de realizar una compra por S/. 3000.00', '2024-11-09 00:32:11', 1),
(25, 1, 49, 'El usuario \"Roger\" acaba de realizar una compra por S/. 2500.00', '2024-11-09 18:45:33', 0),
(26, 1, 50, 'El usuario \"Roger\" acaba de realizar una compra por S/. 2500.00', '2024-11-09 18:47:06', 0),
(27, 1, 51, 'El usuario \"Roger\" acaba de realizar una compra por S/. 1200.00', '2024-11-09 18:58:03', 0),
(28, 3, 52, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 1200.00', '2024-11-09 18:58:32', 0),
(29, 1, 53, 'El usuario \"Roger\" acaba de realizar una compra por S/. 100.00', '2024-11-13 23:35:14', 0),
(30, 3, 54, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 800.99', '2024-11-15 23:23:43', 0),
(31, 1, 55, 'El usuario \"Roger\" acaba de realizar una compra por S/. 3000.00', '2024-11-16 20:03:54', 0),
(32, 1, 56, 'El usuario \"Roger\" acaba de realizar una compra por S/. 2500.00', '2024-11-16 20:06:41', 0),
(33, 1, 57, 'El usuario \"Roger\" acaba de realizar una compra por S/. 2000.00', '2024-11-16 20:09:33', 0),
(34, 1, 59, 'El usuario \"Roger\" acaba de realizar una compra por S/. 6700.00', '2024-11-17 01:14:16', 0),
(35, 3, 60, 'El usuario \"Abraham\" acaba de realizar una compra por S/. 300.00', '2024-11-23 19:42:16', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opiniones`
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
-- Volcado de datos para la tabla `opiniones`
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
-- Estructura de tabla para la tabla `paises`
--

CREATE TABLE `paises` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo_iso` varchar(2) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_modificacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `paises`
--

INSERT INTO `paises` (`id`, `nombre`, `codigo_iso`, `activo`, `fecha_creacion`, `fecha_modificacion`) VALUES
(1, 'Perú', 'PE', 1, '2024-11-15 21:08:54', '2024-11-15 21:08:54'),
(10, 'Argentina', 'AR', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(11, 'Brasil', 'BR', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(12, 'Chile', 'CL', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(13, 'Colombia', 'CO', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(14, 'México', 'MX', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(15, 'Uruguay', 'UY', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58'),
(16, 'Venezuela', 'VE', 1, '2024-11-15 23:19:58', '2024-11-15 23:19:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `direccion_id` int(11) NOT NULL,
  `fecha_pedido` datetime NOT NULL DEFAULT current_timestamp(),
  `estado` varchar(20) NOT NULL,
  `metodo_pago_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id`, `usuario_id`, `direccion_id`, `fecha_pedido`, `estado`, `metodo_pago_id`) VALUES
(1, 1, 1, '2024-10-16 22:03:32', 'pendiente', NULL),
(5, 1, 1, '2024-10-16 22:13:08', 'pendiente', NULL),
(6, 1, 1, '2024-10-16 22:14:20', 'pendiente', NULL),
(7, 1, 1, '2024-10-16 22:15:36', 'pendiente', NULL),
(8, 1, 1, '2024-10-16 22:15:52', 'pendiente', NULL),
(9, 1, 1, '2024-10-16 22:49:19', 'pendiente', NULL),
(10, 1, 1, '2024-10-16 23:10:06', 'pendiente', NULL),
(13, 1, 1, '2024-10-18 20:04:12', 'pendiente', NULL),
(14, 1, 1, '2024-10-22 19:01:55', 'pendiente', NULL),
(15, 1, 1, '2024-10-22 19:06:06', 'pendiente', NULL),
(16, 1, 1, '2024-10-22 19:06:33', 'pendiente', NULL),
(17, 1, 1, '2024-10-22 19:08:41', 'pendiente', NULL),
(18, 1, 1, '2024-10-22 20:11:36', 'pendiente', NULL),
(19, 3, 12, '2024-10-22 20:24:35', 'pendiente', NULL),
(20, 3, 12, '2024-10-22 20:26:18', 'pendiente', NULL),
(21, 3, 7, '2024-10-22 00:00:00', 'NV', NULL),
(22, 3, 13, '2024-10-22 00:00:00', 'Ferrañafe', NULL),
(24, 1, 1, '2024-10-22 00:00:00', 'Lambayeque', NULL),
(25, 1, 1, '2024-10-23 18:26:58', 'pendiente', NULL),
(26, 1, 14, '2024-10-23 18:32:55', 'pendiente', NULL),
(27, 1, 1, '2024-10-23 00:00:00', 'Lambayequea', NULL),
(28, 1, 14, '2024-10-23 19:49:11', 'pendiente', NULL),
(29, 3, 13, '2024-10-23 19:54:04', 'pendiente', NULL),
(30, 3, 7, '2024-10-23 19:55:10', 'pendiente', NULL),
(31, 3, 13, '2024-10-23 00:00:00', 'MIraflores', NULL),
(32, 1, 14, '2024-10-23 20:08:51', 'pendiente', NULL),
(33, 1, 1, '2024-10-23 20:09:50', 'pendiente', NULL),
(34, 1, 1, '2024-10-23 20:09:53', 'pendiente', NULL),
(35, 1, 1, '2024-10-23 20:09:58', 'pendiente', NULL),
(36, 1, 1, '2024-10-23 20:12:29', 'pendiente', NULL),
(37, 1, 1, '2024-10-23 20:15:54', 'pendiente', NULL),
(38, 1, 14, '2024-10-23 20:20:32', 'pendiente', NULL),
(39, 1, 1, '2024-10-23 20:33:02', 'pendiente', NULL),
(40, 1, 1, '2024-10-24 18:00:45', 'pendiente', NULL),
(41, 1, 1, '2024-10-25 16:30:14', 'pendiente', NULL),
(42, 1, 14, '2024-10-25 16:34:37', 'pendiente', NULL),
(43, 1, 14, '2024-10-25 19:18:01', 'pendiente', NULL),
(44, 1, 1, '2024-11-07 23:06:47', 'pendiente', NULL),
(45, 3, 12, '2024-11-08 17:47:31', 'pendiente', NULL),
(46, 1, 1, '2024-11-08 17:52:53', 'pendiente', NULL),
(47, 1, 1, '2024-11-08 19:15:50', 'pendiente', NULL),
(48, 1, 1, '2024-11-08 19:32:11', 'pendiente', NULL),
(49, 1, 14, '2024-11-09 13:45:33', 'pendiente', NULL),
(50, 1, 1, '2024-11-09 13:47:06', 'pendiente', NULL),
(51, 1, 1, '2024-11-09 13:58:03', 'pendiente', NULL),
(52, 3, 7, '2024-11-09 13:58:32', 'pendiente', NULL),
(53, 1, 1, '2024-11-13 18:35:14', 'pendiente', NULL),
(54, 3, 7, '2024-11-15 18:23:43', 'pendiente', NULL),
(55, 1, 1, '2024-11-16 15:03:54', 'pendiente', 1),
(56, 1, 1, '2024-11-16 15:06:41', 'pendiente', 1),
(57, 1, 1, '2024-11-16 15:09:33', 'pendiente', 1),
(58, 1, 14, '2024-11-16 20:12:47', 'pendiente', 1),
(59, 1, 1, '2024-11-16 20:14:16', 'pendiente', 1),
(60, 3, 7, '2024-11-23 14:42:16', 'pendiente', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `categoria_id` int(11) DEFAULT NULL,
  `id_marca` int(10) DEFAULT NULL,
  `id_modelo` int(10) DEFAULT NULL,
  `destacado` tinyint(1) DEFAULT 0,
  `imagen` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `categoria_id`, `id_marca`, `id_modelo`, `destacado`, `imagen`, `fecha_creacion`) VALUES
(1, 'Iphone 15', 'Descubre la innovación con el iPhone 15, un dispositivo diseñado para redefinir tus expectativas. Con una pantalla Super Retina XDR más brillante y tecnología Dynamic Island, cada interacción se vuelve más intuitiva. Equipado con el potente chip A16 Bionic, asegura un rendimiento ultrarrápido y eficiencia energética. Su cámara de 48 MP eleva la fotografía móvil al siguiente nivel, permitiendo capturar cada momento con una nitidez impresionante. Además, la integración de USB-C facilita la conectividad universal. El iPhone 15 combina diseño elegante y tecnología de vanguardia, listo para acompañarte en cada aventura.', 3000.00, 0, 1, 1, 1, 0, 'Iphone_15.png', '2024-11-23 19:19:53'),
(2, 'Iphone 12', 'El iPhone 12 sigue destacando como un clásico moderno, ofreciendo la combinación perfecta entre estilo y rendimiento. Con una pantalla OLED Super Retina XDR y el poderoso chip A14 Bionic, brinda una experiencia fluida para multitareas y juegos. Su sistema de cámara dual captura fotos vibrantes y vídeos en 4K, mientras que su diseño con bordes planos aporta elegancia y durabilidad. Compatible con 5G y con carga rápida MagSafe, el iPhone 12 es una opción sólida para los amantes de la tecnología que buscan calidad y eficiencia en un solo dispositivo.', 2300.00, 0, 1, 1, 2, 0, 'Iphone_12.png', '2024-11-23 19:19:53'),
(3, 'Apple Watch SE', 'El Apple Watch SE combina las mejores funciones esenciales del Apple Watch con un diseño moderno y accesible. Perfecto para llevar un estilo de vida activo, ofrece seguimiento avanzado de actividad física, notificaciones de frecuencia cardíaca y detección de caídas. Su integración con watchOS permite acceder a aplicaciones, responder mensajes y controlar tu música desde la muñeca. Compatible con Apple Fitness+, este reloj inteligente se convierte en tu aliado ideal para alcanzar metas de salud y bienestar. Además, su diseño ligero y personalizable con correas intercambiables lo convierte en el complemento perfecto para cualquier ocasión.', 1200.00, 0, 2, 1, 3, 0, 'applewatch_se.jpg', '2024-11-23 19:19:53'),
(4, 'Airpods Max', 'Sumérgete en una experiencia de sonido única con los AirPods Max. Diseñados con una combinación perfecta de lujo y tecnología, estos audífonos inalámbricos ofrecen un audio envolvente con cancelación activa de ruido y modo de sonido ambiente para mantenerte conectado con tu entorno cuando lo necesites. Equipados con controladores dinámicos diseñados por Apple, brindan una calidad de sonido excepcional con graves profundos y agudos cristalinos. Su diadema de malla transpirable y almohadillas de espuma viscoelástica garantizan comodidad durante horas de uso. Con Audio Espacial y compatibilidad con Siri, los AirPods Max son la opción perfecta para quienes buscan disfrutar de la música y el entretenimiento sin compromisos.', 2500.00, 0, 3, 1, 4, 0, 'airpods_max.jpg', '2024-11-23 19:19:53'),
(5, 'PS5 Slim', 'Vive la próxima generación de videojuegos con la PS5 Slim, la versión más compacta y elegante de la consola insignia de Sony. Manteniendo el poder del hardware original, esta consola ofrece gráficos impresionantes en 4K HDR, tiempos de carga ultrarrápidos gracias al SSD de alta velocidad, y compatibilidad con ray tracing para una inmersión visual sin precedentes. Su diseño más delgado y ligero se adapta perfectamente a cualquier espacio. Además, con acceso a juegos exclusivos de PlayStation y el servicio PS Plus, la PS5 Slim es ideal para quienes buscan potencia y estilo en una consola de nueva generación.', 2000.00, 0, 4, 3, 5, 0, 'ps5_slim.jpg', '2024-11-23 19:19:53'),
(6, 'God of War Ragnarok', 'Embárcate en una épica aventura con God of War: Ragnarök, la esperada secuela que sigue la historia de Kratos y su hijo Atreus mientras enfrentan el fin de los tiempos en la mitología nórdica. Con un impresionante mundo abierto, gráficos mejorados en 4K y combates más fluidos, este título ofrece una experiencia inmersiva llena de desafíos y momentos inolvidables. Explora los nueve reinos y enfréntate a nuevos dioses y criaturas míticas mientras Kratos lidia con su destino como guerrero y padre. La jugabilidad combina acción intensa, resolución de acertijos y un profundo desarrollo narrativo que te atrapará desde el primer momento.\r\n\r\nPrepárate para desafiar el destino y enfrentar a los dioses en esta emocionante obra maestra exclusiva de PlayStation.', 200.00, 48, 5, NULL, NULL, 0, 'god_of_war_ragnarok.jpg', '2024-11-23 19:19:53'),
(7, 'Crash Twinsanity', 'videojuego antiguos', 200.00, 97, 5, NULL, NULL, 0, 'crash.jpg', '2024-11-23 19:19:53'),
(10, 'Iphone XR', 'un celular', 800.99, 19, 1, NULL, NULL, 0, 'iphone_xr.jpg', '2024-11-23 19:19:53'),
(11, 'GTA V', 'Videojuego', 100.00, 6, 5, NULL, NULL, 0, 'gtav.jpg', '2024-11-23 19:19:53');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `tipo` enum('cliente','administrador') DEFAULT 'cliente',
  `foto` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `contrasena`, `tipo`, `foto`, `fecha_registro`) VALUES
(1, 'Roger', 'Zavaleta', 'meencantas7u7@gmail.com', '$2b$12$SYr0n45Sj9X4fM1zzIYUZO9SJtAq7XNATT.BUxrKWEro4qmtAWtoG', 'administrador', 'cliente2.jpg', '2024-10-17 00:46:55'),
(3, 'Abraham', 'Vidaurre', 'cliente@gmail.com', '$2b$12$NSXzq1c8RksnOj6pk6pCYer4Z88Eno93fCTcMrWfG.VSKJ/qBfR1m', 'cliente', NULL, '2024-10-18 18:16:52');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciudades`
--
ALTER TABLE `ciudades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ciudades_estado` (`estado_id`);

--
-- Indices de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `direcciones`
--
ALTER TABLE `direcciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_direcciones_distrito` (`distrito_id`),
  ADD KEY `idx_direcciones_ubicacion` (`cached_ubicacion_id`);

--
-- Indices de la tabla `distritos`
--
ALTER TABLE `distritos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_distritos_ciudad` (`ciudad_id`);

--
-- Indices de la tabla `estados`
--
ALTER TABLE `estados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_estados_pais` (`pais_id`);

--
-- Indices de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `geocoding_cache`
--
ALTER TABLE `geocoding_cache`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_geocoding_direccion` (`direccion_completa`(255));

--
-- Indices de la tabla `kits`
--
ALTER TABLE `kits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `celular_id` (`celular_id`),
  ADD KEY `funda_id` (`smartwatch_id`),
  ADD KEY `audifonos_id` (`accesorios_id`);

--
-- Indices de la tabla `marcas`
--
ALTER TABLE `marcas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `metodos_pago`
--
ALTER TABLE `metodos_pago`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `modelos`
--
ALTER TABLE `modelos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `pedido_id` (`pedido_id`);

--
-- Indices de la tabla `opiniones`
--
ALTER TABLE `opiniones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `paises`
--
ALTER TABLE `paises`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_iso` (`codigo_iso`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `direccion_id` (`direccion_id`),
  ADD KEY `metodo_pago_id` (`metodo_pago_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `categoria_id` (`categoria_id`),
  ADD KEY `idMarca` (`id_marca`),
  ADD KEY `idModelo` (`id_modelo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `ciudades`
--
ALTER TABLE `ciudades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT de la tabla `direcciones`
--
ALTER TABLE `direcciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `distritos`
--
ALTER TABLE `distritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `estados`
--
ALTER TABLE `estados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `geocoding_cache`
--
ALTER TABLE `geocoding_cache`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `kits`
--
ALTER TABLE `kits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `marcas`
--
ALTER TABLE `marcas`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `metodos_pago`
--
ALTER TABLE `metodos_pago`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `modelos`
--
ALTER TABLE `modelos`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `opiniones`
--
ALTER TABLE `opiniones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `paises`
--
ALTER TABLE `paises`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ciudades`
--
ALTER TABLE `ciudades`
  ADD CONSTRAINT `ciudades_ibfk_1` FOREIGN KEY (`estado_id`) REFERENCES `estados` (`id`);

--
-- Filtros para la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD CONSTRAINT `detalles_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`),
  ADD CONSTRAINT `detalles_pedido_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `direcciones`
--
ALTER TABLE `direcciones`
  ADD CONSTRAINT `direcciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `direcciones_ibfk_2` FOREIGN KEY (`distrito_id`) REFERENCES `distritos` (`id`),
  ADD CONSTRAINT `direcciones_ibfk_3` FOREIGN KEY (`cached_ubicacion_id`) REFERENCES `geocoding_cache` (`id`);

--
-- Filtros para la tabla `distritos`
--
ALTER TABLE `distritos`
  ADD CONSTRAINT `distritos_ibfk_1` FOREIGN KEY (`ciudad_id`) REFERENCES `ciudades` (`id`);

--
-- Filtros para la tabla `estados`
--
ALTER TABLE `estados`
  ADD CONSTRAINT `estados_ibfk_1` FOREIGN KEY (`pais_id`) REFERENCES `paises` (`id`);

--
-- Filtros para la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `favoritos_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `kits`
--
ALTER TABLE `kits`
  ADD CONSTRAINT `kits_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `kits_ibfk_2` FOREIGN KEY (`celular_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `kits_ibfk_3` FOREIGN KEY (`smartwatch_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `kits_ibfk_4` FOREIGN KEY (`accesorios_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `metodos_pago`
--
ALTER TABLE `metodos_pago`
  ADD CONSTRAINT `metodos_pago_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `notificaciones_ibfk_2` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`);

--
-- Filtros para la tabla `opiniones`
--
ALTER TABLE `opiniones`
  ADD CONSTRAINT `opiniones_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`),
  ADD CONSTRAINT `opiniones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`direccion_id`) REFERENCES `direcciones` (`id`),
  ADD CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodos_pago` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_marca`) REFERENCES `marcas` (`id`),
  ADD CONSTRAINT `productos_ibfk_3` FOREIGN KEY (`id_modelo`) REFERENCES `modelos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;