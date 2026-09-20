from videojuegos.aventura import JuegoAventura
from videojuegos.competitivo import JuegoCompetitivo
from videojuegos.terror import JuegoTerror
from videojuegos.gestor_videojuegos import GestorVideojuegos
from videojuegos.estrategia import JuegoEstrategia
from videojuegos.educativo import JuegoEducativo
from videojuegos.shooter import JuegoDisparos

from basededatos.conexion import conectar


gestor = GestorVideojuegos()


def obtener_opciones(tabla):
    consultas = {"generos": "SELECT id_genero, nombre FROM Generos ORDER BY id_genero",
        "plataformas": "SELECT id_plataforma, nombre FROM Plataformas ORDER BY id_plataforma",
        "desarrolladores": "SELECT id_desarrollador, nombre FROM Desarrolladores ORDER BY id_desarrollador",
        "tipos": "SELECT id_tipo, nombre FROM TiposVideojuego ORDER BY id_tipo"
    }

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(consultas[tabla])
    opciones = cursor.fetchall()

    conexion.close()

    return opciones


def seleccionar_opcion(titulo, opciones):
    print(f"\n--- {titulo} ---")

    for posicion, opcion in enumerate(opciones, start=1):
        print(f"{posicion}. {opcion[1]}")

    while True:
        try:
            seleccion = int(input("Seleccione una opción: "))

            if 1 <= seleccion <= len(opciones):
                return opciones[seleccion - 1][1]

            print("Opción no válida.")

        except ValueError:
            print("Digite un número.")


def registrar_videojuego():

    print("\n--- REGISTRAR VIDEOJUEGO ---")

    nombre = input("Digite el nombre del videojuego: ")

    genero = seleccionar_opcion(
        "SELECCIONE EL GÉNERO",
        obtener_opciones("generos")
    )

    plataforma = seleccionar_opcion(
        "SELECCIONE LA PLATAFORMA",
        obtener_opciones("plataformas")
    )

    anio_lanzamiento = int(
        input("Ingrese el año de lanzamiento: ")
    )

    precio = float(
        input("Ingrese el precio: ")
    )

    desarrollador = seleccionar_opcion(
        "SELECCIONE EL DESARROLLADOR",
        obtener_opciones("desarrolladores")
    )

    tipos = obtener_opciones("tipos")

    tipo_nombre = seleccionar_opcion("SELECCIONE EL TIPO DE VIDEOJUEGO", tipos)

    constructores = {
        "JuegoAventura": JuegoAventura,
        "JuegoCompetitivo": JuegoCompetitivo,
        "JuegoTerror": JuegoTerror,
        "JuegoEstrategia": JuegoEstrategia,
        "JuegoEducativo": JuegoEducativo,
        "JuegoDisparos": JuegoDisparos
    }

    if tipo_nombre not in constructores:
        print("El tipo de videojuego no tiene una clase asociada.")
        return

    clase_videojuego = constructores[tipo_nombre]

    juego = clase_videojuego(
        nombre,
        genero,
        plataforma,
        anio_lanzamiento,
        precio,
        desarrollador
    )

    gestor.agregar_videojuego(juego)


while True:

    print("\n========== GAMEHUB ==========")
    print("1. Registrar videojuego")
    print("2. Mostrar videojuegos")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_videojuego()

    elif opcion == "2":
        gestor.mostrar_videojuegos()

    elif opcion == "3":
        print("\nPrograma finalizado.")
        break

    else:
        print("\nOpción no válida.")