from basededatos.conexion import consultar, ejecutar
from notificaciones.notificacion import Notificacion


class GestorNotificaciones:

    def enviar(self, id_usuario, mensaje):
        # Le manda UN aviso a UNA persona (la columna admite máximo 300 letras)
        mensaje = mensaje[:300]
        ejecutar("INSERT INTO Notificaciones (id_usuario, mensaje) VALUES (?, ?)", (id_usuario, mensaje))

    def enviar_a_administradores(self, mensaje):
        # Le manda el aviso a cada administrador, uno por uno
        for fila in consultar("SELECT id_usuario FROM Usuarios WHERE rol = 'admin'"):
            self.enviar(fila[0], mensaje)

    def listar(self, id_usuario):
        filas = consultar("""SELECT id_notificacion, id_usuario, mensaje, leida FROM Notificaciones
                             WHERE id_usuario = ? ORDER BY id_notificacion DESC""", (id_usuario,))
        avisos = []
        for fila in filas:
            avisos.append(Notificacion(fila[1], fila[2], fila[3] == 1, fila[0]))
        return avisos

    def contar_sin_leer(self, id_usuario):
        filas = consultar("SELECT COUNT(*) FROM Notificaciones WHERE id_usuario = ? AND leida = 0", (id_usuario,))
        return filas[0][0]

    def marcar_leida(self, id_notificacion, id_usuario):
        # Marca UNA notificación (solo si es de esa persona)
        ejecutar("UPDATE Notificaciones SET leida = 1 WHERE id_notificacion = ? AND id_usuario = ?",
                 (id_notificacion, id_usuario))
