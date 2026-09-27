class Usuario:
    def __init__(self, nombre, telefono, correo, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        