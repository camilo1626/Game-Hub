class Videojuego:
    # Clase PADRE: un videojuego físico que alguien publica

    Estados = ["Nuevo", "Bueno", "Regular"]
    Ofertas = ["Venta", "Intercambio", "Donación"]

    def __init__(self, nombre, genero, plataforma, año_lanzamiento, precio, desarrollador,
                 estado, tipo_oferta, id_usuario, id_videojuego=None):
        if año_lanzamiento < 1970 or año_lanzamiento > 2026:
            raise ValueError("El año de lanzamiento no es válido")
        self.id_videojuego = id_videojuego
        self.nombre = nombre
        self.genero = genero
        self.plataforma = plataforma
        self.año_lanzamiento = año_lanzamiento
        self.desarrollador = desarrollador
        self.estado = estado
        self.tipo_oferta = tipo_oferta
        self.id_usuario = id_usuario        # dueño del juego
        self.dueno = ""                     # nombre del dueño (para mostrarlo)
        self.disponible = True
        self.imagen = ""                    # link de la portada (opcional)
        self.__precio = 0                   # privado (encapsulamiento)
        self.cambiar_precio(precio)

    def obtener_precio(self):
        return self.__precio

    def cambiar_precio(self, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.tipo_oferta != "Venta":
            precio = 0                      # intercambio y donación no cobran
        self.__precio = precio

    def jugar(self):
        return "Estoy jugando " + self.nombre
