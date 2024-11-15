import requests
from datetime import datetime, timedelta
from clase.clase_geocoding_cache import GeocodingCache
import json
from bd import obtener_conexion
import logging

class ControladorGeocoding:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conexion = obtener_conexion()
        self.api_key = "TU_API_KEY_AQUI"  # Reemplazar con tu API key

    def geocodificar_direccion(self, direccion_completa):
        try:
            # Primero buscar en caché
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM geocoding_cache 
                WHERE direccion_completa = %s 
                    AND fecha_expiracion > NOW() 
                    AND activo = true
            """, (direccion_completa,))
            
            cached = cursor.fetchone()
            if cached:
                return GeocodingCache.from_db_row(cached)

            # Si no está en caché, consultar API
            response = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json',
                params={
                    'address': direccion_completa,
                    'key': self.api_key
                }
            )

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    location = data['results'][0]['geometry']['location']
                    
                    # Guardar en caché
                    cursor.execute("""
                        INSERT INTO geocoding_cache (
                            direccion_completa, latitud, longitud, 
                            datos_api, fecha_expiracion
                        ) VALUES (%s, %s, %s, %s, %s)
                        RETURNING *
                    """, (
                        direccion_completa,
                        location['lat'],
                        location['lng'],
                        json.dumps(data),
                        datetime.now() + timedelta(days=30)
                    ))
                    self.conexion.commit()
                    
                    return GeocodingCache.from_db_row(cursor.fetchone())

            return None
            
        except Exception as e:
            self.logger.error(f"Error en geocodificación: {str(e)}")
            return None
        finally:
            cursor.close()