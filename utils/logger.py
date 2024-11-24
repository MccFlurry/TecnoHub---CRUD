import logging
import os
from datetime import datetime

# Configurar el logger
def setup_logger():
    # Crear el directorio de logs si no existe
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Crear un nuevo archivo de log cada día
    log_filename = os.path.join(log_dir, f'tecnohub_{datetime.now().strftime("%Y%m%d")}.log')

    # Configurar el formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configurar el manejador de archivo
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    # Configurar el logger
    logger = logging.getLogger('tecnohub')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

# Crear una instancia del logger
logger = setup_logger()

def log_info(message):
    """Log información general"""
    logger.info(message)

def log_error(message, error=None):
    """Log errores con detalles adicionales"""
    if error:
        logger.error(f"{message}: {str(error)}")
    else:
        logger.error(message)

def log_warning(message):
    """Log advertencias"""
    logger.warning(message)

def log_debug(message):
    """Log información de depuración"""
    logger.debug(message)

def log_api_call(method, endpoint, status_code, message=None):
    """Log llamadas a la API con método, endpoint, código de estado y mensaje opcional"""
    log_message = f"API Call - {method} {endpoint} - Status: {status_code}"
    if message:
        log_message += f" - Message: {message}"
    logger.info(log_message)

def log_database_operation(operation, table, status, message=None):
    """Log operaciones de base de datos"""
    log_message = f"Database Operation - {operation} on {table} - Status: {status}"
    if message:
        log_message += f", Message: {message}"
    logger.info(log_message)
