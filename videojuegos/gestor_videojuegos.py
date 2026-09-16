class GestorVideojuegos:
    def __init__(self):
        self.videojuegos = []

    def agregar_videojuego(self, videojuego):
        self.videojuegos.append(videojuego)

    def mostrar_videojuegos(self):
        if len(self.videojuegos) == 0:
            print("No hay videojuegos registrados.")
            return

        for videojuego in self.videojuegos:
            videojuego.jugar()
            print("Nombre:", videojuego.nombre)
            print("Género:", videojuego.obtener_genero())
            print("Plataforma:",videojuego.obtener_plataforma())
            print("año lanzamiento:",videojuego.obtener_año_lanzamiento())
            print("precio:",videojuego.obtener_precio())
            print("desarrollador:",videojuego.obtener_desarrollador())
            print("------------------")