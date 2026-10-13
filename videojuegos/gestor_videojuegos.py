from basededatos.conexion import conectar, consultar, ejecutar
from videojuegos.Juegos.tipos import TIPOS

# Trae el juego con los nombres de su género, plataforma, desarrollador, tipo y dueño
CONSULTA = """
    SELECT v.id_videojuego, v.nombre, g.nombre, p.nombre, v.año_lanzamiento, v.precio,
           d.nombre, t.nombre, v.estado, v.tipo_oferta, v.id_usuario, u.nombre, v.disponible, v.imagen
    FROM Videojuegos v
    INNER JOIN Generos g ON v.id_genero = g.id_genero
    INNER JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
    INNER JOIN Desarrolladores d ON v.id_desarrollador = d.id_desarrollador
    INNER JOIN TiposVideojuego t ON v.id_tipo = t.id_tipo
    INNER JOIN Usuarios u ON v.id_usuario = u.id_usuario
"""


class GestorVideojuegos:
    # CRUD de la tabla Videojuegos

    def crear_objetos(self, filas):
        juegos = []
        for fila in filas:
            clase = TIPOS[fila[7]]          # elige la clase hija según el tipo
            juego = clase(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6],
                          fila[8], fila[9], fila[10], fila[0])
            juego.dueno = fila[11]
            juego.disponible = fila[12] == 1
            juego.imagen = fila[13] or ""
            juegos.append(juego)
        return juegos

    # C - Create
    def agregar(self, juego):
        ejecutar("""
            INSERT INTO Videojuegos (nombre, id_genero, id_plataforma, año_lanzamiento, precio,
                                     id_desarrollador, id_tipo, estado, tipo_oferta, id_usuario, imagen)
            VALUES (?,
                    (SELECT id_genero FROM Generos WHERE nombre = ?),
                    (SELECT id_plataforma FROM Plataformas WHERE nombre = ?),
                    ?, ?,
                    (SELECT id_desarrollador FROM Desarrolladores WHERE nombre = ?),
                    (SELECT id_tipo FROM TiposVideojuego WHERE nombre = ?),
                    ?, ?, ?, ?)
        """, (juego.nombre, juego.genero, juego.plataforma,
              juego.año_lanzamiento, juego.obtener_precio(), juego.desarrollador,
              juego.tipo, juego.estado, juego.tipo_oferta, juego.id_usuario, juego.imagen))

    # R - Read
    def listar_todos(self):
        return self.crear_objetos(consultar(CONSULTA + " ORDER BY v.id_videojuego DESC"))

    def listar_disponibles(self):
        return self.crear_objetos(consultar(CONSULTA + " WHERE v.disponible = 1 ORDER BY v.id_videojuego DESC"))

    def listar_de_usuario(self, id_usuario):
        return self.crear_objetos(consultar(CONSULTA + " WHERE v.id_usuario = ?", (id_usuario,)))

    def buscar(self, id_videojuego):
        juegos = self.crear_objetos(consultar(CONSULTA + " WHERE v.id_videojuego = ?", (id_videojuego,)))
        if len(juegos) == 0:
            return None
        return juegos[0]

    # U - Update
    def tiene_venta(self, id_videojuego):
        # True si el juego ya tiene un pedido ACEPTADO (historial)
        filas = consultar("""
            SELECT COUNT(*) FROM Solicitudes s
            WHERE s.id_videojuego = ? AND s.estado = 'Aceptada'
        """, (id_videojuego,))
        return filas[0][0] > 0

    def actualizar_precio(self, juego):
        # El precio solo cambia si el juego SIGUE disponible y no tiene un pedido aceptado.
        # La condición va dentro del UPDATE, así nadie la puede saltar aunque acepten un pedido al mismo tiempo.
        cambiadas = ejecutar("""
            UPDATE Videojuegos SET precio = ?
            WHERE id_videojuego = ? AND disponible = 1
              AND NOT EXISTS (SELECT 1 FROM Solicitudes WHERE id_videojuego = ? AND estado = 'Aceptada')
        """, (juego.obtener_precio(), juego.id_videojuego, juego.id_videojuego))
        if cambiadas != 1:
            raise ValueError("No puedes cambiar el precio: el juego está reservado o tiene una compra aceptada.")

    def actualizar_imagen(self, juego):
        ejecutar("UPDATE Videojuegos SET imagen = ? WHERE id_videojuego = ?",
                 (juego.imagen, juego.id_videojuego))

    def marcar_entregado(self, id_videojuego):
        # (Ya no se usa al aceptar: ahora GestorSolicitudes.aceptar() reserva el juego en una transacción)
        ejecutar("UPDATE Videojuegos SET disponible = 0 WHERE id_videojuego = ?", (id_videojuego,))

    # D - Delete
    def eliminar(self, id_videojuego):
        # Primero se borra lo que depende del juego: las solicitudes
        # Todo en UNA transacción: si algo falla, no queda nada borrado a medias
        conexion = conectar()
        try:
            cursor = conexion.cursor()
            # 1. Primero se "toma" la fila del juego (mismo orden que aceptar una solicitud: juego -> solicitudes).
            #    Así, si alguien acepta un pedido al mismo tiempo, uno espera al otro en vez de bloquearse los dos.
            cursor.execute("UPDATE Videojuegos SET disponible = disponible WHERE id_videojuego = ?", (id_videojuego,))
            # 2. Si ya hay un pedido aceptado, NO se borra: se conserva el historial
            cursor.execute("""
                SELECT COUNT(*) FROM Solicitudes s
                WHERE s.id_videojuego = ? AND s.estado = 'Aceptada'
            """, (id_videojuego,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar: este juego ya tiene un pedido aceptado (historial).")
            # 3. Se borra lo que depende del juego y después el juego
            cursor.execute("DELETE FROM Solicitudes WHERE id_videojuego = ?", (id_videojuego,))
            cursor.execute("DELETE FROM Videojuegos WHERE id_videojuego = ?", (id_videojuego,))
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()
