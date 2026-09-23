import sqlite3

def conectar():
    conexion = sqlite3.connect("gamehub.db")
    return conexion


def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videojuegos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            genero TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tabla()
    print("Base de datos y tabla creadas correctamente")