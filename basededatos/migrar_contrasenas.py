import os
import sys

from werkzeug.security import generate_password_hash, check_password_hash

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CARPETA_PROYECTO)

from basededatos.conexion import conectar


def tiene_hash(texto):
    return (texto or "").startswith(("scrypt:", "pbkdf2:"))


def revisar(cursor):
    cursor.execute("SELECT id_usuario, correo, contrasena FROM Usuarios ORDER BY id_usuario")
    filas = cursor.fetchall()
    viejas = []
    for fila in filas:
        if not tiene_hash(fila[2]):
            viejas.append(fila)
    return filas, viejas


def main():
    aplicar = "--aplicar" in sys.argv
    conexion = conectar()
    cursor = conexion.cursor()

    # La columna debe tener espacio para el hash
    cursor.execute("SELECT COL_LENGTH('Usuarios', 'contrasena')")
    if cursor.fetchone()[0] < 510:
        print("La columna contrasena es muy pequeña para el hash.")
        print("Primero ejecuta:  python basededatos/crear_base.py   (no borra datos)")
        conexion.close()
        return

    filas, viejas = revisar(cursor)
    print("Usuarios en total:", len(filas))
    print("Cuentas con contraseña SIN hash:", len(viejas))
    for fila in viejas:
        print("   -", fila[1])           # solo el correo, nunca la contraseña

    if len(viejas) == 0:
        print("No hay nada que migrar.")
        conexion.close()
        return
    if not aplicar:
        print()
        print("Esto fue solo una revisión: NO se cambió nada.")
        print("Cuando tengas la copia de seguridad, ejecuta:  python basededatos/migrar_contrasenas.py --aplicar")
        conexion.close()
        return

    try:
        for id_usuario, correo, contrasena in viejas:
            nuevo = generate_password_hash(contrasena)
            cursor.execute("UPDATE Usuarios SET contrasena = ? WHERE id_usuario = ? AND contrasena = ?",
                           (nuevo, id_usuario, contrasena))
            if cursor.rowcount != 1:
                raise RuntimeError("La cuenta " + correo + " cambió mientras se migraba")

        # Comprobaciones ANTES de guardar
        cursor.execute("SELECT id_usuario, contrasena FROM Usuarios")
        guardadas = {}
        for fila in cursor.fetchall():
            guardadas[fila[0]] = fila[1]
        if len(guardadas) != len(filas):
            raise RuntimeError("El número de usuarios cambió")
        for id_usuario, correo, contrasena in viejas:
            if not check_password_hash(guardadas[id_usuario], contrasena):
                raise RuntimeError("El hash de " + correo + " no se pudo comprobar")

        conexion.commit()
        print("Listo: se migraron", len(viejas), "cuentas. Los usuarios entran con la MISMA contraseña de siempre.")
    except Exception as error:
        conexion.rollback()
        print("No se migró nada (se deshicieron los cambios):", error)
    finally:
        conexion.close()


if __name__ == "__main__":
    main()
