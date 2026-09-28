class Videojuego:
    Estados = ["Nuevo","Bueno","Regular"]
    Ofertas = ["Venta","Intercambio","Donación"]
    def __init__(self, nombre, genero,plataforma,año_lanzamiento,precio,desarrollador,estado="Bueno",
                tipo_oferta="Venta",id_usuario=None,id_videojuego=None):
        self.nombre = nombre
        self.__genero = genero
        self.__plataforma = plataforma
        self.__año_lanzamiento = año_lanzamiento
        self.__precio= precio
        self.__desarrollador = desarrollador
        self.__estado = estado 
        self.__tipo_oferta = tipo_oferta
        self.__id_usuario = id_usuario
        self.__id_videojuego = id_videojuego

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

    def obtener_estado(self):
        return self.__estado

    def obtener_tipo_oferta(self):
        return self.__tipo_oferta

    def obtener_id_usuario(self):
        return self.__id_usuario

    def obtener_id_videojuego(self):
        return self.__id_videojuego

    def cambiar_nombre(self, nombre):
        if nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        self.nombre = nombre

    def cambiar_genero(self, genero):
        self.__genero = genero

    def cambiar_plataforma(self, plataforma):
        self.__plataforma = plataforma

    def cambiar_año_lanzamiento(self, año_lanzamiento):
        if año_lanzamiento < 1950:
            raise ValueError("El año de lanzamiento no es válido")
        self.__año_lanzamiento = año_lanzamiento

    def cambiar_precio(self, precio):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__precio = precio

    def cambiar_desarrollador(self, desarrollador):
        self.__desarrollador = desarrollador

    def cambiar_estado(self, estado):
        if estado not in Videojuego.Estados:
            raise ValueError("Estado no válido")
        self.__estado = estado

    def cambiar_tipo_oferta(self, tipo_oferta):
        if tipo_oferta not in Videojuego.Ofertas:
            raise ValueError("Tipo de oferta no válido")
        self.__tipo_oferta = tipo_oferta

    def jugar(self):
        print("Estoy jugando", self.nombre)
    
    