# GameHub

Página web comunitaria para que los jóvenes de Fusagasugá vendan, intercambien o donen videojuegos físicos usados.
Hecha con HTML + CSS, Python (POO) con Flask y SQL Server.

## Cómo ejecutarlo (en la terminal de VS Code, dentro de la carpeta GameHub-web)

1. Instalar las librerías (incluye **Flask-WTF**, que protege los formularios contra CSRF):
   ```
   pip install -r requirements.txt
   ```
2. Crear la clave secreta **una sola vez** (PowerShell):
   ```
   setx GAMEHUB_SECRET_KEY (python -c "import secrets; print(secrets.token_hex(32))")
   ```
   Cierra VS Code por completo y ábrelo otra vez (así toma la variable). Sin esta clave la página no enciende.
3. **Copia de seguridad** de la base (antes de actualizarla): abre `basededatos/respaldo.sql` en SQL Server
   Management Studio y ejecútalo (F5). No cambia nada; solo crea `GameHub_respaldo.bak`.
4. Crear o actualizar la base de datos (**no borra datos**: solo crea lo que falta y agranda la columna de la contraseña):
   ```
   python basededatos/crear_base.py
   ```
   Si la base está vacía, agrega las cuentas y juegos de prueba (con la contraseña protegida con hash).
5. Contraseñas viejas (opcional): primero revisa, luego aplica.
   ```
   python basededatos/migrar_contrasenas.py
   python basededatos/migrar_contrasenas.py --aplicar
   ```
   Los usuarios siguen entrando con la misma contraseña. Si no lo ejecutas, cada cuenta se convierte sola al iniciar sesión.
6. Encender la página:
   ```
   python main.py
   ```
7. Entrar en el navegador a http://127.0.0.1:5000

## Seguridad

- La clave secreta se lee de la variable de entorno `GAMEHUB_SECRET_KEY` (no está en el código).
- `debug` está apagado: nadie ve el código ni los errores internos.
- Las contraseñas se guardan como **hash** (Werkzeug), nunca como texto.
- Todos los formularios llevan `csrf_token` (Flask-WTF `CSRFProtect`).
- El rol de administrador se revisa en la base de datos en cada acción de administrador.
- Aceptar un pedido es una **transacción**: no se pueden aceptar dos pedidos del mismo juego.
- Si algo falla, la página muestra un mensaje amable, sin detalles de SQL Server.

## Portadas de los juegos

Cada juego puede tener una imagen de portada (opcional): al publicarlo, o en **Mis juegos → Portada**,
se pega el link de una imagen (en el navegador: clic derecho sobre una imagen → *Copiar dirección de imagen*).
Si no tiene portada, se muestra el ícono de su tipo de juego.

## Cuentas de prueba y demostración pública

| Rol           | Correo             | Contraseña |
|---------------|--------------------|------------|
| Administrador | admin@gamehub.com  | **la que pongas tú** (no se escribe en documentos) |
| Usuario       | juan@gamehub.com   | 1234 (cámbiala antes de la demo pública) |
| Usuario       | camilo@gamehub.com | 1234 (cámbiala antes de la demo pública) |

Antes de compartir el link público:
1. Contraseña del administrador (obligatorio: `main.py` no enciende la página si un admin usa una contraseña conocida
   como `admin123`). Mínimo 10 caracteres, con letras y números:
   ```
   python basededatos/cambiar_contrasena.py admin@gamehub.com
   ```
2. Recomendado: cambia también las de Juan y Camilo, porque `1234` aparece en documentos del proyecto:
   ```
   python basededatos/cambiar_contrasena.py juan@gamehub.com
   python basededatos/cambiar_contrasena.py camilo@gamehub.com
   ```
La contraseña no se ve mientras la escribes (es normal). El script solo cambia esa contraseña: no borra nada.

## Roles

- **Visitante:** ve el inicio y el catálogo.
- **Usuario:** publica juegos, pide juegos, acepta o rechaza pedidos y recibe notificaciones.
- **Administrador:** ve todos los usuarios, juegos y solicitudes, y puede eliminar publicaciones.

## Documentación

En la carpeta `documentacion/` están:
- `GUIA_EXPOSICION.md`: explicación de cada clase y método, los pilares de POO, la metodología de prototipado y el paso a paso de la demostración.
- `diagrama_clases.png`: diagrama UML de clases.
- `diagrama_casos_uso.png`: diagrama UML de casos de uso (visitante, usuario y administrador).
