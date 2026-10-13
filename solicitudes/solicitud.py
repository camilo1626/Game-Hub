class Solicitud:
    # Cuando un usuario pide el juego de otro usuario

    def __init__(self, id_videojuego, id_solicitante, mensaje, estado="Pendiente", id_solicitud=None):
        self.id_solicitud = id_solicitud
        self.id_videojuego = id_videojuego
        self.id_solicitante = id_solicitante
        self.mensaje = mensaje
        self.estado = estado
        self.nombre_juego = ""          # para mostrar en pantalla
        self.nombre_solicitante = ""    # para mostrar en pantalla
        self.id_dueno = None            # dueño del juego pedido
