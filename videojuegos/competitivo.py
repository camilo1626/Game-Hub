from .videojuego import Videojuego


class JuegoCompetitivo(Videojuego):

    def __init__(self, nombre, genero):
        super().__init__(nombre, genero)

    def jugar(self):
        print(self.nombre, "es un juego competitivo.")