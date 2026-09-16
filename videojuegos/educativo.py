from .videojuego import Videojuego

class JuegoEducativo(Videojuego):
    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador):
        super().__init__(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador)

    def jugar(self):
        print ( "es un juego educativo")