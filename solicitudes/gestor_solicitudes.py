from basededatos.conexion import conectar, consultar, ejecutar
from solicitudes.solicitud import Solicitud

# Trae la solicitud con el nombre del juego y el nombre de quien lo pidió
CONSULTA = """
    SELECT s.id_solicitud, s.id_videojuego, s.id_solicitante, s.mensaje, s.estado,
           v.nombre, u.nombre, v.id_usuario
    FROM Solicitudes s
    INNER JOIN Videojuegos v ON s.id_videojuego = v.id_videojuego
    INNER JOIN Usuarios u ON s.id_solicitante = u.id_usuario
"""


class GestorSolicitudes:

    def crear_objetos(self, filas):
        lista = []
        for fila in filas:
            solicitud = Solicitud(fila[1], fila[2], fila[3], fila[4], fila[0])
            solicitud.nombre_juego = fila[5]
            solicitud.nombre_solicitante = fila[6]
            solicitud.id_dueno = fila[7]
            lista.append(solicitud)
        return lista

    def agregar(self, solicitud):
        mensaje = (solicitud.mensaje or "").strip()
        if len(mensaje) > 200:
            raise ValueError("El mensaje es muy largo (máximo 200 caracteres)")
        solicitud.mensaje = mensaje
        ejecutar("INSERT INTO Solicitudes (id_videojuego, id_solicitante, mensaje) VALUES (?, ?, ?)",
                 (solicitud.id_videojuego, solicitud.id_solicitante, solicitud.mensaje))

    def buscar(self, id_solicitud):
        lista = self.crear_objetos(consultar(CONSULTA + " WHERE s.id_solicitud = ?", (id_solicitud,)))
        if len(lista) == 0:
            return None
        return lista[0]

    def listar_recibidas(self, id_dueno):
        # Pedidos que le hicieron a MIS juegos
        return self.crear_objetos(consultar(CONSULTA + " WHERE v.id_usuario = ? ORDER BY s.id_solicitud DESC", (id_dueno,)))

    def listar_enviadas(self, id_solicitante):
        # Pedidos que YO hice
        return self.crear_objetos(consultar(CONSULTA + " WHERE s.id_solicitante = ? ORDER BY s.id_solicitud DESC", (id_solicitante,)))

    def listar_todas(self):
        # Para el administrador
        return self.crear_objetos(consultar(CONSULTA + " ORDER BY s.id_solicitud DESC"))

    def tiene_pendiente(self, id_videojuego, id_solicitante):
        # Evita que la misma persona pida el mismo juego dos veces
        filas = consultar("""SELECT COUNT(*) FROM Solicitudes
                             WHERE id_videojuego = ? AND id_solicitante = ? AND estado = 'Pendiente'""",
                          (id_videojuego, id_solicitante))
        return filas[0][0] > 0

    def aceptar(self, id_solicitud, id_videojuego):
        # TRANSACCIÓN: o se hacen los 3 pasos completos, o no se hace ninguno.
        # Devuelve la lista de personas cuyos pedidos se rechazaron automáticamente.
        #
        # ORDEN DE LOS PASOS (para evitar interbloqueos o "deadlocks"):
        # Siempre se toca PRIMERO el juego y DESPUÉS las solicitudes.
        # Si dos personas aceptan pedidos del mismo juego al mismo tiempo, la segunda
        # se queda esperando en el paso 1 hasta que la primera termine; nunca se esperan
        # la una a la otra al mismo tiempo (eso es un interbloqueo).
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            # 1. El juego queda RESERVADO (sale del catálogo), solo si SIGUE disponible
            cursor.execute("UPDATE Videojuegos SET disponible = 0 WHERE id_videojuego = ? AND disponible = 1",
                           (id_videojuego,))
            if cursor.rowcount != 1:
                raise ValueError("Este juego ya no está disponible: ya se aceptó otra solicitud.")
            # 2. Solo se acepta si la solicitud SIGUE pendiente y es de ESE juego
            cursor.execute("""UPDATE Solicitudes SET estado = 'Aceptada'
                              WHERE id_solicitud = ? AND id_videojuego = ? AND estado = 'Pendiente'""",
                           (id_solicitud, id_videojuego))
            if cursor.rowcount != 1:
                raise ValueError("Esta solicitud ya fue respondida.")   # el rollback devuelve el juego a disponible
            # 3. Los demás pedidos pendientes de ese juego se rechazan
            cursor.execute("SELECT id_solicitante FROM Solicitudes WHERE id_videojuego = ? AND estado = 'Pendiente'",
                           (id_videojuego,))
            rechazados = []
            for fila in cursor.fetchall():
                rechazados.append(fila[0])
            cursor.execute("UPDATE Solicitudes SET estado = 'Rechazada' WHERE id_videojuego = ? AND estado = 'Pendiente'",
                           (id_videojuego,))
            conexion.commit()          # todo salió bien: se guardan los cambios
            return rechazados
        except ValueError:
            conexion.rollback()        # una comprobación falló: se deshace todo
            raise
        except Exception as error:
            conexion.rollback()        # algo falló: se deshace todo
            # 40001 = SQL Server eligió esta transacción como "víctima" de un interbloqueo
            if "40001" in str(error) or "1205" in str(error):
                raise ValueError("GameHub estaba ocupado con otra respuesta. Intenta aceptar otra vez.")
            raise
        finally:
            conexion.close()

    def rechazar(self, id_solicitud):
        # Solo se puede rechazar si sigue pendiente
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("UPDATE Solicitudes SET estado = 'Rechazada' WHERE id_solicitud = ? AND estado = 'Pendiente'",
                           (id_solicitud,))
            if cursor.rowcount != 1:
                raise ValueError("Esta solicitud ya fue respondida.")
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def cambiar_estado(self, id_solicitud, estado):
        ejecutar("UPDATE Solicitudes SET estado = ? WHERE id_solicitud = ?", (estado, id_solicitud))
