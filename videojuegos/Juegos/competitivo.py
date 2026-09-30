from videojuegos.Juegos.videojuego import Videojuego


class JuegoCompetitivo(Videojuego):

    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador, estado="Bueno", tipo_oferta="Venta", id_usuario=None, id_videojuego=None):
        super().__init__(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador, estado, tipo_oferta, id_usuario, id_videojuego)
        self.tipo = "JuegoCompetitivo"

    def jugar(self):
        print(self.nombre, "es un juego competitivo.")