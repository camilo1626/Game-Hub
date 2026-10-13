from .videojuego import Videojuego

class JuegoTerror(Videojuego):
    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador):
        super().__init__(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador)

    def jugar(self):
        print (" Es un juego de terror")