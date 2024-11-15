# clase/clase_direcciones.py

class Direcciones:
    def __init__(self, id=None, usuario_id=None, direccion=None, ciudad=None, 
                 estado=None, pais=None, codigo_postal=None, distrito_id=None,
                 latitud=None, longitud=None, direccion_predeterminada=False,
                 numero=None, departamento=None):
        self.id = id
        self.usuario_id = usuario_id
        self.direccion = direccion
        self.ciudad = ciudad
        self.estado = estado
        self.pais = pais
        self.codigo_postal = codigo_postal
        self.distrito_id = distrito_id
        self.latitud = latitud
        self.longitud = longitud
        self.direccion_predeterminada = direccion_predeterminada
        self.numero = numero
        self.departamento = departamento
        
        # Campos para relaciones
        self._distrito = None
        self._ciudad = None
        self._estado = None
        self._pais = None

    def set_ubicacion_jerarquica(self, distrito, ciudad, estado, pais):
        self._distrito = distrito
        self._ciudad = ciudad
        self._estado = estado
        self._pais = pais

    @property
    def direccion_completa(self):
        partes = []
        if self.direccion:
            partes.append(self.direccion)
        if self.numero:
            partes.append(self.numero)
        if self.departamento:
            partes.append(f"Dpto. {self.departamento}")
        if self.ciudad:
            partes.append(self.ciudad)
        if self.estado:
            partes.append(self.estado)
        if self.pais:
            partes.append(self.pais)
        if self.codigo_postal:
            partes.append(f"CP: {self.codigo_postal}")
        return ", ".join(partes)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'estado': self.estado,
            'pais': self.pais,
            'codigo_postal': self.codigo_postal,
            'distrito_id': self.distrito_id,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'direccion_predeterminada': self.direccion_predeterminada,
            'numero': self.numero,
            'departamento': self.departamento,
            'direccion_completa': self.direccion_completa,
            'distrito': self._distrito.to_dict() if self._distrito else None,
            'ciudad_obj': self._ciudad.to_dict() if self._ciudad else None,
            'estado_obj': self._estado.to_dict() if self._estado else None,
            'pais_obj': self._pais.to_dict() if self._pais else None
        }

    @staticmethod
    def from_db_row(row):
        if not row:
            return None
            
        return Direcciones(
            id=row[0] if len(row) > 0 else None,
            usuario_id=row[1] if len(row) > 1 else None,
            direccion=row[2] if len(row) > 2 else None,
            ciudad=row[3] if len(row) > 3 else None,
            estado=row[4] if len(row) > 4 else None,
            pais=row[5] if len(row) > 5 else None,
            codigo_postal=row[6] if len(row) > 6 else None,
            distrito_id=row[7] if len(row) > 7 else None,
            latitud=row[8] if len(row) > 8 else None,
            longitud=row[9] if len(row) > 9 else None,
            direccion_predeterminada=bool(row[10]) if len(row) > 10 else False,
            numero=row[11] if len(row) > 11 else None,
            departamento=row[12] if len(row) > 12 else None,
        )

    @staticmethod
    def from_dict(data):
        return Direcciones(
            id=data.get('id'),
            usuario_id=data.get('usuario_id'),
            direccion=data.get('direccion'),
            ciudad=data.get('ciudad'),
            estado=data.get('estado'),
            pais=data.get('pais'),
            codigo_postal=data.get('codigo_postal'),
            distrito_id=data.get('distrito_id'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            direccion_predeterminada=data.get('direccion_predeterminada', False),
            numero=data.get('numero'),
            departamento=data.get('departamento'),
        )