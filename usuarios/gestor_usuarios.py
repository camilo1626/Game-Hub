from basededatos.conexion import consultar, ejecutar


class GestorUsuarios:

    def agregar(self, usuario):
        ejecutar("INSERT INTO Usuarios (nombre, telefono, correo) VALUES (?, ?, ?)",
                (usuario.nombre, usuario.telefono, usuario.correo))

    def listar(self):
        return consultar("SELECT id_usuario, nombre, telefono, correo FROM Usuarios")

    def actualizar(self, usuario):
        ejecutar("UPDATE Usuarios SET nombre = ?, telefono = ?, correo = ? WHERE id_usuario = ?",
                (usuario.nombre, usuario.telefono, usuario.correo, usuario.id_usuario))

    def eliminar(self, id_usuario):
        ejecutar("DELETE FROM Solicitudes WHERE id_solicitante = ?", (id_usuario,))
        ejecutar("DELETE FROM Videojuegos WHERE id_usuario = ?", (id_usuario,))
        ejecutar("DELETE FROM Usuarios WHERE id_usuario = ?", (id_usuario,))
