class Videojuego:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.__genero = genero

    def jugar(self):
        print("Estoy jugando", self.nombre)

    def obtener_genero(self):
        return self.__genero