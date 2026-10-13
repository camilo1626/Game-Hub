from usuarios.usuario import Usuario


class Administrador(Usuario):

    def __init__(self, nombre, correo, telefono, contrasena, id_usuario=None):
        super().__init__(nombre, correo, telefono, contrasena, id_usuario)
        self.rol = "admin"

    def es_admin(self):
        return True

    def descripcion(self):
        return "Puedes ver todos los usuarios, juegos y solicitudes."