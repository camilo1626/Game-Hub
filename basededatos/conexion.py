import pyodbc


def conectar():
    conexion = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=GameHub;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return conexion


def crear_tabla():
    pass


if __name__ == "__main__":
    conexion = conectar()
    print("Conexión a SQL Server correcta")
    conexion.close()