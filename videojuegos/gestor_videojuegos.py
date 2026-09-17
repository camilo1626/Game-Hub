from basededatos.conexion import conectar, crear_tabla


class GestorVideojuegos:

    def __init__(self):
        self.videojuegos = []
        crear_tabla()

    def agregar_videojuego(self, videojuego):
        self.videojuegos.append(videojuego)

        nombre = videojuego.nombre
        genero = videojuego.obtener_genero()
        tipo = videojuego.__class__.__name__


        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO videojuegos (nombre, genero, tipo)
            VALUES (?, ?, ?)
        """, (nombre, genero, tipo))

        conexion.commit()
        conexion.close()

        print("Videojuego guardado correctamente en la base de datos.")

    def mostrar_videojuegos(self):
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, genero, tipo
            FROM videojuegos
        """)

        videojuegos = cursor.fetchall()
        conexion.close()

        if len(videojuegos) == 0:
            print("No hay videojuegos registrados.")
            return

        print("\n--- VIDEOJUEGOS REGISTRADOS ---")

        for videojuego in videojuegos:
            id_videojuego, nombre, genero, tipo = videojuego

            print("ID:", id_videojuego)
            print("Nombre:", nombre)
            print("Género:", genero)
            print("Tipo:", tipo)
            print("------------------")