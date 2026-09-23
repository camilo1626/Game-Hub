from videojuegos.aventura import JuegoAventura
from videojuegos.competitivo import JuegoCompetitivo
from videojuegos.terror import JuegoTerror
from videojuegos.gestor_videojuegos import GestorVideojuegos
from videojuegos.estrategia import JuegoEstrategia
from videojuegos.educativo import JuegoEducativo
from videojuegos.shooter import JuegoDisparos


gestor = GestorVideojuegos()


def registrar_videojuego():
    print("\n--- REGISTRAR VIDEOJUEGO ---")

    nombre = input("Digite el nombre del videojuego: ")
    genero = input("Digite el género del videojuego: ")
    plataforma = input("ingrese la plataforma: ")
    año_lanzamiento = input("ingrese el año lanzamiento: ")
    precio = input("ingrese el precio: ")
    desarrollador = input("ingrese el desarrollador: ")


    print("\nSeleccione el tipo de videojuego:")
    print("1. Aventura")
    print("2. Competitivo")
    print("3. Terror")
    print("4. Estrategia")
    print("5. Educativo")
    print("6. Shooter")



    tipo = input("Digite una opción: ")

    if tipo == "1":
        juego = JuegoAventura(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador)

    elif tipo == "2":
        juego = JuegoCompetitivo(nombre, genero, plataforma, año_lanzamiento, precio, desarrollador)

    elif tipo == "3":
        juego = JuegoTerror(nombre,genero, plataforma, año_lanzamiento, precio, desarrollador)

    elif tipo == "4":
        juego = JuegoEstrategia(nombre,genero,plataforma,año_lanzamiento,precio,desarrollador)

    elif tipo == "5":
        juego = JuegoEducativo(nombre,genero,plataforma,año_lanzamiento,precio,desarrollador)

    elif tipo == "6":
        juego = JuegoDisparos(nombre,genero,plataforma,año_lanzamiento,precio,desarrollador)

    else:
        print("Opción no válida.")
        return

    gestor.agregar_videojuego(juego)
    print("Videojuego registrado correctamente.")


while True:

    print("\n========== GAMEHUB ==========")
    print("1. Registrar videojuego")
    print("2. Mostrar videojuegos")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_videojuego()

    elif opcion == "2":
        print("\n--- VIDEOJUEGOS REGISTRADOS ---")
        gestor.mostrar_videojuegos()

    elif opcion == "3":
        print("\nPrograma finalizado.")
        break

    else:

        print("\nOpción no válida.")
        print("\nOcion validaa.")

    print("Cambio realizado desde mi computador")
    print("\nOpción no válida.")
    print("Modificacion realizada por Camilo")