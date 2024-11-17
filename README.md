# TecnoHub - Sistema de Gestión de Productos Tecnológicos

TecnoHub es una aplicación web completa para la gestión de productos tecnológicos, que incluye sistema de usuarios, categorías, productos, pedidos y más funcionalidades.

## 🚀 Características

- Gestión de usuarios y autenticación
- Catálogo de productos tecnológicos
- Sistema de categorías y marcas
- Gestión de pedidos
- Sistema de favoritos
- Opiniones y valoraciones
- Sistema de notificaciones
- Gestión de direcciones y ubicaciones
- Integración con servicios de geocodificación
- Métodos de pago
- Sistema de kits de productos

## 🛠️ Tecnologías Utilizadas

- **Backend**: 
  - Python (Flask)
  - PHP (Servicios adicionales)
  - MySQL
- **Frontend**:
  - HTML/CSS
  - JavaScript
  - Node.js para dependencias frontend

## 📋 Requisitos Previos

- Python 3.x
- PHP 7.x o superior
- MySQL
- Node.js y npm

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/MccFlurry/TecnoHub---CRUD.git
cd TecnoHub---CRUD
```

2. Instala las dependencias de Python:
```bash
pip install -r requirements.txt
```

3. Instala las dependencias de Node.js:
```bash
npm install
```

4. Configura la base de datos:
- Importa el archivo `py_paginaweb.sql` en tu servidor MySQL
- Configura las credenciales de la base de datos en `bd.py` y `bd.php`

5. Inicia el servidor:
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
TecnoHub---CRUD/
├── main.py                     # Punto de entrada principal
├── bd.py                      # Configuración de base de datos Python
├── bd.php                     # Configuración de base de datos PHP
├── controlador_*.py           # Controladores para diferentes funcionalidades
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
├── templates/                 # Plantillas HTML
├── clase/                    # Clases y modelos
└── node_modules/             # Dependencias de Node.js
```

## 🔐 Controladores Principales

- `controlador_usuario.py`: Gestión de usuarios y autenticación
- `controlador_producto.py`: Gestión de productos
- `controlador_pedido.py`: Gestión de pedidos
- `controlador_direcciones.py`: Gestión de direcciones
- `controlador_notificaciones.py`: Sistema de notificaciones
- `controlador_geocoding.py`: Servicios de geocodificación
- `controlador_kit.py`: Gestión de kits de productos

## 🔄 Flujo de Trabajo

1. Los usuarios pueden registrarse y autenticarse
2. Navegar por el catálogo de productos
3. Agregar productos a favoritos
4. Realizar pedidos
5. Gestionar direcciones de envío
6. Recibir notificaciones
7. Dejar opiniones y valoraciones