import os

from basededatos.conexion import probar_conexion, base_actualizada

if len(os.environ.get("GAMEHUB_SECRET_KEY", "")) < 32:
    print("Falta la variable de entorno GAMEHUB_SECRET_KEY (o es muy corta).")
    print("Créala UNA sola vez en la terminal de VS Code (PowerShell) con este comando:")
    print('    setx GAMEHUB_SECRET_KEY (python -c "import secrets; print(secrets.token_hex(32))")')
    print("Después cierra VS Code por completo, ábrelo otra vez y vuelve a ejecutar:  python main.py")
    raise SystemExit(1)

from app import app
from usuarios.gestor_usuarios import GestorUsuarios

conectado, error = probar_conexion()

if not conectado:
    print("No se pudo conectar con SQL Server:")
    print(error)
elif not base_actualizada():
    print("La base de datos GameHub es de una versión vieja.")
    print("1. Haz primero la copia de seguridad (mira basededatos/respaldo.sql).")
    print("2. Actualízala con este comando (NO borra tus datos) y vuelve a intentar:")
    print("    python basededatos/crear_base.py")
elif len(GestorUsuarios().admins_con_contrasena_conocida()) > 0:
    print("Por seguridad la página NO se encendió.")
    print("Estos administradores tienen una contraseña conocida:")
    for correo in GestorUsuarios().admins_con_contrasena_conocida():
        print("    -", correo)
    print("Cámbiala con este comando y vuelve a intentar:")
    print("    python basededatos/cambiar_contrasena.py admin@gamehub.com")
else:
    app.run(debug=False)