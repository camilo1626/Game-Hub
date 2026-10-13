# Muestra en la terminal todas las personas registradas en GameHub (sin mostrar contraseñas)
# Uso (desde la carpeta GameHub-web):   python basededatos/ver_usuarios.py

from conexion import consultar

filas = consultar("SELECT id_usuario, nombre, correo, telefono, contrasena, rol FROM Usuarios ORDER BY id_usuario")

print()
print("PERSONAS REGISTRADAS EN GAMEHUB:", len(filas))
print("-" * 100)
print(f"{'ID':<4}{'Nombre':<22}{'Correo':<30}{'Teléfono':<14}{'Contraseña':<18}{'Rol'}")
print("-" * 100)

for fila in filas:
    if str(fila[4]).startswith(("scrypt:", "pbkdf2:")):
        estado = "Protegida"
    else:
        estado = "SIN hash"
    print(f"{fila[0]:<4}{str(fila[1]):<22}{str(fila[2]):<30}{str(fila[3]):<14}{estado:<18}{fila[5]}")

print("-" * 100)
