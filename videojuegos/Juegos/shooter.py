from videojuegos.Juegos.videojuego import Videojuego

class JuegoDisparos(Videojuego):
    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador, estado="Bueno", tipo_oferta="Venta", id_usuario=None, id_videojuego=None):
        super().__init__(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador, estado, tipo_oferta, id_usuario, id_videojuego)

    def jugar(self):
        print(self.nombre, "es un juego de disparos.")