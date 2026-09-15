from videojuegos.aventura import JuegoAventura
from videojuegos.competitivo import JuegoCompetitivo
from videojuegos.gestor_videojuegos import GestorVideojuegos


gestor = GestorVideojuegos()


def registrar_videojuego():
    print("\n--- REGISTRAR VIDEOJUEGO ---")

    nombre = input("Digite el nombre del videojuego: ")
    genero = input("Digite el género del videojuego: ")

    print("\nSeleccione el tipo de videojuego:")
    print("1. Aventura")
    print("2. Competitivo")

    tipo = input("Digite una opción: ")

    if tipo == "1":
        juego = JuegoAventura(nombre, genero)

    elif tipo == "2":
        juego = JuegoCompetitivo(nombre, genero)

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
        print("\nOcion validaa.")

    print("Cambio realizado desde mi computador")