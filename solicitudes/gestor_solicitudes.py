from basededatos.conexion import consultar, ejecutar


class GestorSolicitudes:

    def agregar(self, solicitud):
        ejecutar("INSERT INTO Solicitudes (id_videojuego, id_solicitante, juego_ofrecido) VALUES (?, ?, ?)",
                 (solicitud.id_videojuego, solicitud.id_solicitante, solicitud.juego_ofrecido))

    def listar_recibidas(self, id_usuario):
        return consultar("""
            SELECT s.id_solicitud, v.nombre, u.nombre, u.telefono, s.juego_ofrecido, s.estado
            FROM Solicitudes s
            INNER JOIN Videojuegos v ON s.id_videojuego = v.id_videojuego
            INNER JOIN Usuarios u ON s.id_solicitante = u.id_usuario
            WHERE v.id_usuario = ?
        """, (id_usuario,))

    def listar_enviadas(self, id_usuario):
        return consultar("""
            SELECT s.id_solicitud, v.nombre, u.nombre, u.telefono, s.juego_ofrecido, s.estado
            FROM Solicitudes s
            INNER JOIN Videojuegos v ON s.id_videojuego = v.id_videojuego
            INNER JOIN Usuarios u ON v.id_usuario = u.id_usuario
            WHERE s.id_solicitante = ?
        """, (id_usuario,))

    def aceptar(self, id_solicitud):
        ejecutar("UPDATE Solicitudes SET estado = 'Aceptada' WHERE id_solicitud = ?", (id_solicitud,))
        ejecutar("""
            UPDATE Videojuegos SET disponible = 0
            WHERE id_videojuego = (SELECT id_videojuego FROM Solicitudes WHERE id_solicitud = ?)
        """, (id_solicitud,))

    def rechazar(self, id_solicitud):
        ejecutar("UPDATE Solicitudes SET estado = 'Rechazada' WHERE id_solicitud = ?", (id_solicitud,))

    def eliminar(self, id_solicitud):
        ejecutar("DELETE FROM Solicitudes WHERE id_solicitud = ?", (id_solicitud,))
