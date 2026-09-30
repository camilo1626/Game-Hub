from basededatos.conexion import consultar, ejecutar
from videojuegos.Juegos.tipos import TIPOS

CONSULTA = """
    SELECT v.id_videojuego, v.nombre, g.nombre, p.nombre, v.año_lanzamiento, v.precio,
           d.nombre, t.nombre, v.estado, v.tipo_oferta, v.id_usuario
    FROM Videojuegos v
    INNER JOIN Generos g ON v.id_genero = g.id_genero
    INNER JOIN Plataformas p ON v.id_plataforma = p.id_plataforma
    INNER JOIN Desarrolladores d ON v.id_desarrollador = d.id_desarrollador
    INNER JOIN TiposVideojuego t ON v.id_tipo = t.id_tipo
"""


class GestorVideojuegos:

    def convertir(self, filas):
        juegos = []
        for fila in filas:
            clase = TIPOS[fila[7]]
            juego = clase(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6],
                          fila[8], fila[9], fila[10], fila[0])
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
        """, (juego.nombre, juego.genero, juego.plataforma,
              juego.año_lanzamiento, juego.obtener_precio(), juego.desarrollador,
              juego.tipo, juego.estado, juego.tipo_oferta, juego.id_usuario))

    def listar_todos(self):
        filas = consultar(CONSULTA + " ORDER BY v.id_videojuego DESC")
        return self.convertir(filas)

    def buscar(self, id_videojuego):
        filas = consultar(CONSULTA + " WHERE v.id_videojuego = ?", (id_videojuego,))
        return self.convertir(filas)[0]

    def actualizar(self, juego):
        ejecutar("UPDATE Videojuegos SET precio = ? WHERE id_videojuego = ?",
                 (juego.obtener_precio(), juego.id_videojuego))

    def eliminar(self, id_videojuego):
        ejecutar("DELETE FROM Solicitudes WHERE id_videojuego = ?", (id_videojuego,))
        ejecutar("DELETE FROM Videojuegos WHERE id_videojuego = ?", (id_videojuego,))
