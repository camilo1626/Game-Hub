from basededatos.conexion import consultar, ejecutar
from videojuegos.Juegos.tipos import TIPOS

CONSULTA = """
    SELECT v.id_videojuego, v.nombre, g.nombre, p.nombre, v.año_lanzamiento, v.precio,
           d.nombre, t.nombre, v.estado, v.tipo_oferta, v.id_usuario, u.nombre
    FROM Videojuegos v
    INNER JOIN Generos g ON v.id_genero = g.id_genero
    INNER JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
    INNER JOIN Desarrolladores d ON v.id_desarrollador = d.id_desarrollador
    INNER JOIN TiposVideojuego t ON v.id_tipo = t.id_tipo
    LEFT JOIN Usuarios u ON v.id_usuario = u.id_usuario
"""


class GestorVideojuegos:

    def convertir(self, filas):
        juegos = []
        for fila in filas:
            clase = TIPOS[fila[7]]
            juego = clase(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6],
                          fila[8], fila[9], fila[10], fila[0])
            juego.nombre_dueno = fila[11] or "Sin dueño"
            juegos.append(juego)
        return juegos

    def agregar(self, juego):
        ejecutar("""
            INSERT INTO Videojuegos (nombre, id_genero, id_plataforma, año_lanzamiento, precio,
                                     id_desarrollador, id_tipo, estado, tipo_oferta, id_usuario)
            VALUES (?,
                    (SELECT id_genero FROM Generos WHERE nombre = ?),
                    (SELECT id_plataforma FROM Plataformas WHERE nombre = ?),
                    ?, ?,
                    (SELECT id_desarrollador FROM Desarrolladores WHERE nombre = ?),
                    (SELECT id_tipo FROM TiposVideojuego WHERE nombre = ?),
                    ?, ?, ?)
        """, (juego.nombre, juego.obtener_genero(), juego.obtener_plataforma(),
              juego.obtener_año_lanzamiento(), juego.obtener_precio(), juego.obtener_desarrollador(),
              type(juego).__name__, juego.obtener_estado(), juego.obtener_tipo_oferta(),
              juego.obtener_id_usuario()))

    def listar_catalogo(self, id_usuario):
        filas = consultar(CONSULTA + " WHERE v.disponible = 1 AND v.id_usuario <> ?", (id_usuario,))
        return self.convertir(filas)

    def listar_por_usuario(self, id_usuario):
        filas = consultar(CONSULTA + " WHERE v.disponible = 1 AND v.id_usuario = ?", (id_usuario,))
        return self.convertir(filas)

    def contar_reutilizados(self):
        filas = consultar("SELECT COUNT(*) FROM Videojuegos WHERE disponible = 0")
        return filas[0][0]

    def actualizar(self, juego):
        ejecutar("""
            UPDATE Videojuegos
            SET nombre = ?, precio = ?, estado = ?, tipo_oferta = ?
            WHERE id_videojuego = ?
        """, (juego.nombre, juego.obtener_precio(), juego.obtener_estado(),
              juego.obtener_tipo_oferta(), juego.obtener_id_videojuego()))

    def eliminar(self, id_videojuego):
        ejecutar("DELETE FROM Solicitudes WHERE id_videojuego = ?", (id_videojuego,))
        ejecutar("DELETE FROM Videojuegos WHERE id_videojuego = ?", (id_videojuego,))
