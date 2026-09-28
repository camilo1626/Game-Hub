class Solicitud:

    def __init__(self, id_videojuego, id_solicitante, juego_ofrecido=None):
        self.id_videojuego = id_videojuego
        self.id_solicitante = id_solicitante
        self.juego_ofrecido = juego_ofrecido
