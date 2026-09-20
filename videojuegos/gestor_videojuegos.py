from basededatos.conexion import conectar, crear_tabla


class GestorVideojuegos:

    def __init__(self):
        self.videojuegos = []
        crear_tabla()

    def agregar_videojuego(self, videojuego):
        self.videojuegos.append(videojuego)

        nombre = videojuego.nombre
        genero = videojuego.obtener_genero()
        plataforma = videojuego.obtener_plataforma()
        anio_lanzamiento = videojuego.obtener_año_lanzamiento()
        precio = videojuego.obtener_precio()
        desarrollador = videojuego.obtener_desarrollador()
        tipo = videojuego.__class__.__name__

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id_genero FROM Generos WHERE nombre = ?",
            (genero,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            conexion.close()
            print("El género no existe en la base de datos.")
            return

        id_genero = resultado[0]


        cursor.execute(
            "SELECT id_plataforma FROM Plataformas WHERE nombre = ?",
            (plataforma,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            conexion.close()
            print("La plataforma no existe en la base de datos.")
            return

        id_plataforma = resultado[0]

        cursor.execute(
            "SELECT id_desarrollador FROM Desarrolladores WHERE nombre = ?",
            (desarrollador,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            conexion.close()
            print("El desarrollador no existe en la base de datos.")
            return

        id_desarrollador = resultado[0]

        cursor.execute(
            "SELECT id_tipo FROM TiposVideojuego WHERE nombre = ?",
            (tipo,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            conexion.close()
            print("El tipo de videojuego no existe en la base de datos.")
            return

        id_tipo = resultado[0]

        cursor.execute("""
            INSERT INTO Videojuegos
            (
                nombre,
                id_genero,
                id_plataforma,
                anio_lanzamiento,
                precio,
                id_desarrollador,
                id_tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            id_genero,
            id_plataforma,
            anio_lanzamiento,
            precio,
            id_desarrollador,
            id_tipo
        ))

        conexion.commit()
        conexion.close()

        print("Videojuego guardado correctamente en SQL Server.")

    def mostrar_videojuegos(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                v.id_videojuego,
                v.nombre,
                g.nombre AS genero,
                p.nombre AS plataforma,
                v.anio_lanzamiento,
                v.precio,
                d.nombre AS desarrollador,
                t.nombre AS tipo
            FROM Videojuegos v
            INNER JOIN Generos g
                ON v.id_genero = g.id_genero
            INNER JOIN Plataformas p
                ON v.id_plataforma = p.id_plataforma
            INNER JOIN Desarrolladores d
                ON v.id_desarrollador = d.id_desarrollador
            INNER JOIN TiposVideojuego t
                ON v.id_tipo = t.id_tipo
        """)

        videojuegos = cursor.fetchall()
        conexion.close()

        if len(videojuegos) == 0:
            print("No hay videojuegos registrados.")
            return

        print("\n--- VIDEOJUEGOS REGISTRADOS ---")

        for videojuego in videojuegos:

            print("ID:", videojuego[0])
            print("Nombre:", videojuego[1])
            print("Género:", videojuego[2])
            print("Plataforma:", videojuego[3])
            print("Año de lanzamiento:", videojuego[4])
            print("Precio:", videojuego[5])
            print("Desarrollador:", videojuego[6])
            print("Tipo:", videojuego[7])
            print("------------------------------")