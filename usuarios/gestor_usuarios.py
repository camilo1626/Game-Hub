import re
from werkzeug.security import generate_password_hash

from basededatos.conexion import consultar, ejecutar
from usuarios.usuario import Usuario
from usuarios.administrador import Administrador

COLUMNAS = "SELECT id_usuario, nombre, correo, telefono, contrasena, rol FROM Usuarios"

# Contraseñas que cualquiera adivina (o que salieron en documentos del proyecto).
# Un ADMINISTRADOR no puede usar ninguna de estas.
CONTRASENAS_CONOCIDAS = ["admin123", "admin", "1234", "12345", "123456", "password", "contraseña", "gamehub"]


class GestorUsuarios:
    # Guarda y busca usuarios en la tabla Usuarios

    def crear_objeto(self, fila):
        # fila = (id_usuario, nombre, correo, telefono, contrasena, rol)
        if fila[5] == "admin":
            return Administrador(fila[1], fila[2], fila[3], fila[4], fila[0])
        return Usuario(fila[1], fila[2], fila[3], fila[4], fila[0])

    def validar_contrasena(self, contrasena):
        if len(contrasena) < 4:
            raise ValueError("La contraseña debe tener mínimo 4 caracteres")
        if len(contrasena) > 128:
            raise ValueError("La contraseña es demasiado larga")

    def validar_contrasena_admin(self, contrasena):
        # El administrador necesita una contraseña más fuerte
        self.validar_contrasena(contrasena)
        if len(contrasena) < 10:
            raise ValueError("La contraseña del administrador debe tener mínimo 10 caracteres")
        if not any(c.isalpha() for c in contrasena) or not any(c.isdigit() for c in contrasena):
            raise ValueError("La contraseña del administrador debe tener letras y números")
        if contrasena.lower() in CONTRASENAS_CONOCIDAS:
            raise ValueError("Esa contraseña es muy conocida, elige otra")

    def admins_con_contrasena_conocida(self):
        # Devuelve los correos de los administradores que todavía usan una contraseña conocida
        correos = []
        for usuario in self.listar():
            if usuario.es_admin():
                for conocida in CONTRASENAS_CONOCIDAS:
                    if usuario.verificar_contrasena(conocida):
                        correos.append(usuario.correo)
                        break
        return correos

    def validar_datos(self, usuario):
        if usuario.nombre == "" or len(usuario.nombre) > 100:
            raise ValueError("Escribe un nombre (máximo 100 caracteres)")
        if len(usuario.correo) > 100 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", usuario.correo):
            raise ValueError("Escribe un correo válido")
        if not re.fullmatch(r"[0-9+ ]{7,20}", usuario.telefono or ""):
            raise ValueError("Escribe un teléfono válido (solo números, de 7 a 20)")
        self.validar_contrasena(usuario.obtener_contrasena())

    def agregar(self, usuario):
        self.validar_datos(usuario)
        if self.buscar_por_correo(usuario.correo) is not None:
            raise ValueError("Ya existe una cuenta con ese correo")
        # Se guarda el HASH, nunca la contraseña escrita
        hash_contrasena = generate_password_hash(usuario.obtener_contrasena())
        ejecutar("INSERT INTO Usuarios (nombre, correo, telefono, contrasena, rol) VALUES (?, ?, ?, ?, ?)",
                 (usuario.nombre, usuario.correo, usuario.telefono, hash_contrasena, usuario.rol))

    def buscar(self, id_usuario):
        filas = consultar(COLUMNAS + " WHERE id_usuario = ?", (id_usuario,))
        if len(filas) == 0:
            return None
        return self.crear_objeto(filas[0])

    def buscar_por_correo(self, correo):
        filas = consultar(COLUMNAS + " WHERE correo = ?", (correo,))
        if len(filas) == 0:
            return None
        return self.crear_objeto(filas[0])

    def listar(self):
        usuarios = []
        for fila in consultar(COLUMNAS + " ORDER BY id_usuario"):
            usuarios.append(self.crear_objeto(fila))
        return usuarios

    def cambiar_contrasena(self, id_usuario, nueva):
        # La usa el administrador cuando alguien olvidó su contraseña
        usuario = self.buscar(id_usuario)
        if usuario is not None and usuario.es_admin():
            self.validar_contrasena_admin(nueva)
        else:
            self.validar_contrasena(nueva)
        ejecutar("UPDATE Usuarios SET contrasena = ? WHERE id_usuario = ?",
                 (generate_password_hash(nueva), id_usuario))

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.buscar_por_correo(correo)
        if usuario is None or not usuario.verificar_contrasena(contrasena):
            return None
        # Migración: si la cuenta era vieja (sin hash), se guarda ya con hash
        if not usuario.tiene_hash():
            ejecutar("UPDATE Usuarios SET contrasena = ? WHERE id_usuario = ?",
                     (generate_password_hash(contrasena), usuario.id_usuario))
        return usuario
