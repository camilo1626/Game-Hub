from werkzeug.security import check_password_hash


class Usuario:
    # Clase PADRE: una persona registrada en GameHub

    def __init__(self, nombre, correo, telefono, contrasena, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.rol = "usuario"
        # Privada (encapsulamiento). Al crear la cuenta es el texto escrito;
        # al leerla de la base de datos es el HASH guardado (nunca la contraseña real).
        self.__contrasena = contrasena or ""

    def obtener_contrasena(self):
        return self.__contrasena

    def tiene_hash(self):
        # Los hashes de Werkzeug empiezan por el nombre del método usado
        return self.__contrasena.startswith(("scrypt:", "pbkdf2:"))

    def verificar_contrasena(self, contrasena):
        if self.tiene_hash():
            return check_password_hash(self.__contrasena, contrasena)
        # Cuenta vieja que todavía tiene la contraseña sin hash:
        # se compara así UNA vez y el gestor la convierte a hash al iniciar sesión.
        return self.__contrasena != "" and self.__contrasena == contrasena

    def es_admin(self):
        return False

    def descripcion(self):
        return "Puedes publicar tus juegos y pedir los de otros."
