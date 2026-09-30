from basededatos.conexion import consultar, ejecutar
from usuarios.usuario import Usuario


class GestorUsuarios:

    def agregar(self, usuario):
        if self.buscar_por_correo(usuario.correo) is not None:
            raise ValueError("Ya existe una cuenta con ese correo")
        if len(usuario.obtener_contrasena()) < 4:
            raise ValueError("La contraseña debe tener mínimo 4 caracteres")
        ejecutar("INSERT INTO Usuarios (nombre, correo, contrasena) VALUES (?, ?, ?)",
                 (usuario.nombre, usuario.correo, usuario.obtener_contrasena()))

    def buscar_por_correo(self, correo):
        filas = consultar("SELECT id_usuario, nombre, correo, contrasena, telefono FROM Usuarios WHERE correo = ?",
                          (correo,))
        if len(filas) == 0:
            return None
        fila = filas[0]
        return Usuario(fila[1], fila[2], fila[3], fila[4], fila[0])

    def listar(self):
        filas = consultar("SELECT id_usuario, nombre, correo, telefono FROM Usuarios ORDER BY nombre")
        personas = []
        for fila in filas:
            personas.append(Usuario(fila[1], fila[2], "", fila[3], fila[0]))
        return personas

    def iniciar_sesion(self, correo, contrasena):
        usuario = self.buscar_por_correo(correo)
        if usuario is not None and usuario.verificar_contrasena(contrasena):
            return usuario
        return None