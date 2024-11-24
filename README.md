# TecnoHub - Sistema de Gestión de Productos Tecnológicos

TecnoHub es una aplicación web completa para la gestión de productos tecnológicos, desarrollada con Flask y MySQL. El sistema proporciona una plataforma robusta para la administración de inventario, ventas y experiencia de usuario en el sector tecnológico.

## Características

- **Gestión de Usuarios**:
  - Registro y autenticación segura
  - Perfiles de usuario personalizables
  - Roles y permisos (Admin, Usuario, Vendedor)
  - Recuperación de contraseña por email

- **Gestión de Productos**:
  - Catálogo completo con filtros avanzados
  - Sistema de categorías y subcategorías
  - Gestión de marcas y modelos
  - Control de stock en tiempo real
  - Imágenes múltiples por producto
  - Especificaciones técnicas detalladas

- **Sistema de Pedidos**:
  - Carrito de compras
  - Proceso de checkout optimizado
  - Seguimiento de pedidos en tiempo real
  - Historial de compras
  - Facturación electrónica

- **Características Adicionales**:
  - Lista de favoritos personalizada
  - Sistema de reseñas y calificaciones
  - Notificaciones en tiempo real
  - Gestión de direcciones con geocodificación
  - Integración con múltiples métodos de pago
  - Sistema de kits y combos de productos

## Tecnologías Utilizadas

### Backend
- **Python 3.x**:
  - Flask: Framework web principal
  - SQLAlchemy: ORM para base de datos
  - Flask-Login: Gestión de sesiones
  - Flask-Mail: Envío de correos
  - WTForms: Validación de formularios

### Frontend
- **HTML5/CSS3**:
  - Bootstrap 5: Framework CSS
  - SASS: Preprocesador CSS
- **JavaScript**:
  - jQuery: Manipulación del DOM
  - AJAX: Peticiones asíncronas
  - SweetAlert2: Notificaciones elegantes
- **Node.js**: Gestión de dependencias frontend

### Base de Datos
- **MySQL 8.0**:
  - Procedimientos almacenados
  - Triggers para automatización
  - Índices optimizados

### Servicios
- Geocodificación para direcciones
- Almacenamiento de imágenes
- Sistema de caché
- API RESTful

## Requisitos Previos

1. **Software Base**:
   - Python 3.8 o superior
   - MySQL 8.0 o superior
   - Node.js 14.x o superior
   - npm 6.x o superior

2. **Configuración del Sistema**:
   - Servidor web compatible con WSGI
   - Permisos de escritura en directorio de uploads
   - Puerto 5000 disponible (configurable)

## Instalación

1. **Preparación del Entorno**:
```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Instalación de Dependencias**:
```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Instalar dependencias Node.js
npm install
```

3. **Configuración de la Base de Datos**:
```bash
# Importar estructura base
mysql -u usuario -p < py_paginaweb.sql
```

4. **Variables de Entorno**:
Crear archivo `.env` con:
```env
FLASK_APP=main.py
FLASK_ENV=development
DB_HOST=localhost
DB_USER=usuario
DB_PASS=contraseña
DB_NAME=py_paginaweb
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_correo@gmail.com
MAIL_PASSWORD=tu_contraseña
```

5. **Iniciar Aplicación**:
```bash
# Modo desarrollo
flask run

# Modo producción
gunicorn -w 4 main:app
```

## Estructura del Proyecto Detallada

```
TecnoHub---CRUD/
├── main.py                    # Aplicación principal Flask
├── config/
│   ├── __init__.py           # Configuraciones generales
│   ├── database.py           # Configuración de base de datos
│   └── mail.py               # Configuración de correo
├── controllers/              # Controladores de la aplicación
│   ├── usuario.py
│   ├── producto.py
│   ├── pedido.py
│   └── ...
├── models/                   # Modelos de datos
│   ├── usuario.py
│   ├── producto.py
│   └── ...
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│   └── uploads/
├── templates/
│   ├── auth/
│   ├── productos/
│   ├── admin/
│   └── ...
├── utils/                    # Utilidades y helpers
│   ├── decorators.py
│   ├── validators.py
│   └── helpers.py
├── tests/                    # Pruebas unitarias
├── requirements.txt          # Dependencias Python
├── package.json             # Dependencias Node.js
└── README.md
```

## Seguridad

- Contraseñas hasheadas con bcrypt
- Protección CSRF en formularios
- Sanitización de entradas
- Rate limiting en API
- Sesiones seguras con Flask-Login
- Validación de datos en frontend y backend

## Rendimiento

- Caché implementado para consultas frecuentes
- Imágenes optimizadas y servidas desde CDN
- Consultas SQL optimizadas
- Lazy loading de imágenes
- Minificación de assets estáticos