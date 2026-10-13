import os
import sys
from getpass import getpass

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CARPETA_PROYECTO)

from usuarios.gestor_usuarios import GestorUsuarios


def main():
    if len(sys.argv) != 2:
        print("Escribe el correo de la cuenta. Ejemplo:")
        print("    python basededatos/cambiar_contrasena.py admin@gamehub.com")
        return

    gestor = GestorUsuarios()
    correo = sys.argv[1].strip().lower()
    usuario = gestor.buscar_por_correo(correo)
    if usuario is None:
        print("No existe una cuenta con el correo", correo)
        return

    print("Cuenta:", usuario.nombre, "-", "Administrador" if usuario.es_admin() else "Usuario")
    if usuario.es_admin():
        print("Para el administrador: mínimo 10 caracteres, con letras y números.")
    nueva = getpass("Nueva contraseña (no se ve al escribir): ")
    repetida = getpass("Escríbela otra vez: ")
    if nueva != repetida:
        print("Las dos contraseñas no son iguales. No se cambió nada.")
        return

    try:
        gestor.cambiar_contrasena(usuario.id_usuario, nueva)
    except ValueError as error:
        print("No se cambió nada:", error)
        return

    # Comprobación: la contraseña nueva sí funciona para iniciar sesión
    if gestor.iniciar_sesion(correo, nueva) is not None:
        print("Listo: la contraseña de", correo, "se cambió y ya funciona para iniciar sesión.")
    else:
        print("Algo salió mal: la contraseña nueva no funcionó. Avísale al equipo.")


if __name__ == "__main__":
    main()
