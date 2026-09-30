class Usuario:
    def __init__(self, nombre, correo, contraseña, telefono=None, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.__contrasena = contraseña

    def obtener_contrasena(self):
        return self.__contrasena

    def verificar_contrasena(self, contraseña):
        return self.__contrasena == contraseña
