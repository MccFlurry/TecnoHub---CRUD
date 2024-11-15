class GeocodingCache:
    def __init__(self, id=None, direccion_completa=None, latitud=None, longitud=None, 
                 datos_api=None, fecha_consulta=None, fecha_expiracion=None, activo=True):
        self.id = id
        self.direccion_completa = direccion_completa
        self.latitud = latitud
        self.longitud = longitud
        self.datos_api = datos_api
        self.fecha_consulta = fecha_consulta
        self.fecha_expiracion = fecha_expiracion
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'direccion_completa': self.direccion_completa,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'datos_api': self.datos_api,
            'fecha_consulta': self.fecha_consulta.isoformat() if self.fecha_consulta else None,
            'fecha_expiracion': self.fecha_expiracion.isoformat() if self.fecha_expiracion else None,
            'activo': self.activo
        }

    @staticmethod
    def from_db_row(row):
        """
        Crea una instancia de GeocodingCache a partir de una fila de la base de datos
        """
        if not row:
            return None
            
        return GeocodingCache(
            id=row.get('id'),
            direccion_completa=row.get('direccion_completa'),
            latitud=row.get('latitud'),
            longitud=row.get('longitud'),
            datos_api=row.get('datos_api'),
            fecha_consulta=row.get('fecha_consulta'),
            fecha_expiracion=row.get('fecha_expiracion'),
            activo=bool(row.get('activo'))
        )