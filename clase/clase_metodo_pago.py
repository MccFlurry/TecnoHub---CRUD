from datetime import datetime

class MetodoPago:
    def __init__(self, id=None, usuario_id=None, tipo=None, numero_tarjeta=None, 
                 titular=None, fecha_vencimiento=None, cvv=None, predeterminado=0,
                 fecha_registro=None, activo=1):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.numero_tarjeta = numero_tarjeta
        self.titular = titular
        self.fecha_vencimiento = fecha_vencimiento
        self.cvv = cvv
        self.predeterminado = predeterminado
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()
        self.activo = activo

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo': self.tipo,
            'numero_tarjeta': self.numero_tarjeta,
            'titular': self.titular,
            'fecha_vencimiento': self.fecha_vencimiento,
            'cvv': self.cvv,
            'predeterminado': self.predeterminado,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo
        }

    @staticmethod
    def from_dict(data):
        return MetodoPago(
            id=data.get('id'),
            usuario_id=data.get('usuario_id'),
            tipo=data.get('tipo'),
            numero_tarjeta=data.get('numero_tarjeta'),
            titular=data.get('titular'),
            fecha_vencimiento=data.get('fecha_vencimiento'),
            cvv=data.get('cvv'),
            predeterminado=data.get('predeterminado', 0),
            fecha_registro=data.get('fecha_registro'),
            activo=data.get('activo', 1)
        )
