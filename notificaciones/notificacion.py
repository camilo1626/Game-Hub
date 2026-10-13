class Notificacion:
    # Un aviso para UNA persona

    def __init__(self, id_usuario, mensaje, leida=False, id_notificacion=None):
        self.id_notificacion = id_notificacion
        self.id_usuario = id_usuario
        self.mensaje = mensaje
        self.leida = leida
