<?php
class Notificaciones {
    private $id;
    private $usuario_id;
    private $mensaje;
    private $fecha_creacion;
    private $visto;
    private $usuario_nombre;
    private $usuario_foto;

    public function __construct($data) {
        $this->id = $data['id'] ?? null;
        $this->usuario_id = $data['usuario_id'] ?? null;
        $this->mensaje = $data['mensaje'] ?? null;
        $this->fecha_creacion = $data['fecha_creacion'] ?? null;
        $this->visto = $data['visto'] ?? 0;
        $this->usuario_nombre = ($data['nombre'] ?? '') . ' ' . ($data['apellido'] ?? '');
        $this->usuario_foto = $data['foto'] ?? 'default-user.jpg';
    }

    public function serializar() {
        return [
            'id' => $this->id,
            'usuario_id' => $this->usuario_id,
            'mensaje' => $this->mensaje,
            'fecha_creacion' => $this->fecha_creacion,
            'visto' => $this->visto,
            'usuario_nombre' => $this->usuario_nombre,
            'usuario_foto' => $this->usuario_foto
        ];
    }
}