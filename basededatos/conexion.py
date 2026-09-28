import pyodbc

SERVIDOR = "localhost"
BASE_DE_DATOS = "GameHub"
DRIVER = "ODBC Driver 18 for SQL Server"

OPCIONES = {
    "generos": "SELECT nombre FROM Generos ORDER BY id_genero",
    "plataformas": "SELECT nombre FROM Plataformas ORDER BY id_plataforma",
    "desarrolladores": "SELECT nombre FROM Desarrolladores ORDER BY id_desarrollador",
    "tipos": "SELECT nombre FROM TiposVideojuego ORDER BY id_tipo",
}


def conectar():
    return pyodbc.connect(
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVIDOR};"
        f"DATABASE={BASE_DE_DATOS};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )


def probar_conexion():
    try:
        conectar().close()
        return True, ""
    except Exception as error:
        return False, str(error)


def consultar(sql, parametros=()):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, parametros)
    filas = cursor.fetchall()
    conexion.close()
    return filas


def ejecutar(sql, parametros=()):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, parametros)
    conexion.commit()
    conexion.close()


def obtener_opciones(tabla):
    nombres = []
    for fila in consultar(OPCIONES[tabla]):
        nombres.append(fila[0])
    return nombres


if __name__ == "__main__":
    conectado, error = probar_conexion()
    if conectado:
        print("Conexión exitosa con SQL Server")
    else:
        print("Error:", error)
