# Crea o ACTUALIZA la base de datos GameHub SIN BORRAR DATOS.
# Uso (desde la carpeta GameHub-web):   python basededatos/crear_base.py
#
# 1. Ejecuta gamehub.sql: crea lo que falte y agrega columnas nuevas (no usa DROP ni DELETE).
# 2. SOLO si la tabla Usuarios está vacía (base nueva), agrega las cuentas y los juegos de prueba,
#    con las contraseñas guardadas como HASH.
# Antes de usarlo en una base con datos, haz la copia de seguridad (mira respaldo.sql).

import os
import sys

import secrets

import pyodbc
from werkzeug.security import generate_password_hash

# Para poder importar basededatos.conexion aunque se ejecute desde otra carpeta
CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CARPETA_PROYECTO)

from basededatos.conexion import SERVIDOR, DRIVER, conectar

# 1. Leer el archivo gamehub.sql
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gamehub.sql")
archivo = open(ruta, encoding="utf-8")
texto = archivo.read()
archivo.close()

# 2. Conectarse a "master" (porque GameHub puede no existir todavía) y ejecutar por partes (cada parte termina en GO)
conexion = pyodbc.connect(
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVIDOR};"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;",
    autocommit=True,
)
cursor = conexion.cursor()
for parte in texto.split("\nGO"):
    if parte.strip() != "":
        cursor.execute(parte)
conexion.close()
print("Tablas revisadas: se creó o agregó solo lo que faltaba (no se borró nada).")

# 3. Datos de prueba: SOLO si no hay ningún usuario (base de datos nueva)
conexion = conectar()
cursor = conexion.cursor()
cursor.execute("SELECT COUNT(*) FROM Usuarios")
hay_usuarios = cursor.fetchone()[0] > 0

if hay_usuarios:
    print("Ya tienes usuarios guardados: no se agregaron datos de prueba.")
else:
    try:
        cuentas = [
            # El admin recibe una contraseña al azar que NADIE conoce (no se muestra).
            # Después se le pone una propia con:  python basededatos/cambiar_contrasena.py admin@gamehub.com
            ("Administrador", "admin@gamehub.com", "3000000000", secrets.token_urlsafe(24), "admin"),
            ("Juan Garcia", "juan@gamehub.com", "3192695345", "1234", "usuario"),
            ("Camilo Cortes", "camilo@gamehub.com", "3180895981", "1234", "usuario"),
        ]
        for nombre, correo, telefono, contrasena, rol in cuentas:
            cursor.execute("INSERT INTO Usuarios (nombre, correo, telefono, contrasena, rol) VALUES (?, ?, ?, ?, ?)",
                           (nombre, correo, telefono, generate_password_hash(contrasena), rol))

        def id_de(tabla, columna_id, nombre):
            cursor.execute(f"SELECT {columna_id} FROM {tabla} WHERE nombre = ?", (nombre,))
            return cursor.fetchone()[0]

        def id_usuario(correo):
            cursor.execute("SELECT id_usuario FROM Usuarios WHERE correo = ?", (correo,))
            return cursor.fetchone()[0]

        juan = id_usuario("juan@gamehub.com")
        camilo = id_usuario("camilo@gamehub.com")
        juegos = [
            ("GTA V", "Acción", "PlayStation 4", 2013, 80000, "Rockstar Games", "JuegoDisparos", "Bueno", "Venta", juan),
            ("FIFA 23", "Deportes", "PlayStation 4", 2022, 0, "EA Sports", "JuegoCompetitivo", "Nuevo", "Intercambio", juan),
            ("Brain Academy", "Educativo", "Nintendo Switch", 2020, 0, "Nintendo", "JuegoEducativo", "Bueno", "Donación", juan),
            ("Minecraft", "Aventura", "PC", 2011, 40000, "Mojang", "JuegoAventura", "Bueno", "Venta", camilo),
            ("Resident Evil 4", "Terror", "PlayStation 5", 2023, 60000, "Capcom", "JuegoTerror", "Nuevo", "Venta", camilo),
            ("Mario Kart 8", "Carreras", "Nintendo Switch", 2017, 0, "Nintendo", "JuegoCompetitivo", "Regular", "Intercambio", camilo),
        ]
        for nombre, genero, plataforma, anio, precio, desarrollador, tipo, estado, oferta, dueno in juegos:
            cursor.execute("""INSERT INTO Videojuegos (nombre, id_genero, id_plataforma, año_lanzamiento, precio,
                                  id_desarrollador, id_tipo, estado, tipo_oferta, id_usuario)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (nombre, id_de("Generos", "id_genero", genero), id_de("Plataformas", "id_plataforma", plataforma),
                            anio, precio, id_de("Desarrolladores", "id_desarrollador", desarrollador),
                            id_de("TiposVideojuego", "id_tipo", tipo), estado, oferta, dueno))

        # Camilo ya le pidió GTA V a Juan, y le llegó el aviso a Juan
        cursor.execute("SELECT id_videojuego FROM Videojuegos WHERE nombre = 'GTA V'")
        gta = cursor.fetchone()[0]
        cursor.execute("INSERT INTO Solicitudes (id_videojuego, id_solicitante, mensaje) VALUES (?, ?, ?)",
                       (gta, camilo, "Hola, me interesa. ¿Lo entregas en el parque principal?"))
        cursor.execute("INSERT INTO Notificaciones (id_usuario, mensaje) VALUES (?, ?)",
                       (juan, "Camilo Cortes quiere tu juego GTA V. Revisa tus solicitudes."))
        cursor.execute("INSERT INTO Notificaciones (id_usuario, mensaje) VALUES (?, ?)",
                       (id_usuario("admin@gamehub.com"), "Bienvenido al panel del administrador de GameHub."))
        conexion.commit()
        print("Base nueva: se agregaron las cuentas y los juegos de prueba (contraseñas guardadas con hash).")
        print("Ponle contraseña al administrador con:  python basededatos/cambiar_contrasena.py admin@gamehub.com")
    except Exception:
        conexion.rollback()
        print("No se pudieron agregar los datos de prueba. No se guardó ningún cambio de esta parte.")
        raise

conexion.close()
print("Listo. Si tenías contraseñas viejas sin hash, revisa:  python basededatos/migrar_contrasenas.py")
