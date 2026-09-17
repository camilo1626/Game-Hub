class Videojuego:
    def __init__(self, nombre, genero,plataforma,año_lanzamiento,precio,desarrollador):
        self.nombre = nombre
        self.__genero = genero
        self.__plataforma = plataforma
        self.__año_lanzamiento = año_lanzamiento
        self.__precio= precio
        self.__desarrollador = desarrollador

    def jugar(self):
        print("Estoy jugando", self.nombre)

    def obtener_genero(self):
        return self.__genero

    def obtener_plataforma(self):
        return self.__plataforma

    def obtener_año_lanzamiento(self):
        return self.__año_lanzamiento

    def obtener_precio(self):
        return self.__precio

    def obtener_desarrollador(self):
        return self.__desarrollador
    
    