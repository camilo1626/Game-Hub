class Videojuego:
    Estados = ["Nuevo", "Bueno", "Regular"]
    Ofertas = ["Venta", "Intercambio", "Donación"]

    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador,
                 estado="Bueno", tipo_oferta="Venta", id_usuario=None, id_videojuego=None):
        self.nombre = nombre
        self.genero = genero
        self.plataforma = plataforma
        self.año_lanzamiento = año_lanzamiento
        self.desarrollador = desarrollador
        self.estado = estado
        self.tipo_oferta = tipo_oferta
        self.id_usuario = id_usuario
        self.id_videojuego = id_videojuego
        self.__precio = precio

    def obtener_precio(self):
        return self.__precio

    def cambiar_precio(self, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__precio = precio

    def jugar(self):
        print("Estoy jugando", self.nombre)
