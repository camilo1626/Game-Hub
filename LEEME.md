# GameHub

Plataforma web comunitaria para que los jóvenes de Fusagasugá vendan, intercambien o donen videojuegos físicos usados. Hecha con HTML + CSS, Python (POO) con Flask y SQL Server.

## Cómo ejecutarlo

1. En SQL Server ejecutar `basededatos/gamehub.sql` (crea las tablas y datos de ejemplo).
   Si ya tenían la base creada de antes, en vez de eso ejecuten `basededatos/agregar_contrasena.sql` (agrega la columna de contraseña).
   Usuarios de prueba: juan@gamehub.com y camilo@gamehub.com, contraseña 1234.
2. Instalar las librerías:
   ```
   pip install flask pyodbc
   ```
3. Probar la conexión:
   ```
   python basededatos/conexion.py
   ```
4. Abrir la página:
   ```
   python main.py
   ```
   y entrar en el navegador a http://127.0.0.1:5000

## Estructura

```
GameHub/
├── main.py                  prueba la conexión y enciende la web
├── app.py                   rutas Flask: inicio, catálogo, registrar, registrados, editar precio, eliminar, crear cuenta, iniciar y cerrar sesión
├── templates/               páginas HTML
├── static/estilos.css       diseño
├── basededatos/
│   ├── conexion.py          conexión a SQL Server con pyodbc
│   ├── gamehub.sql          tablas y datos de ejemplo
│   ├── datos_ejemplo.sql    juegos de ejemplo (solo si la tabla está vacía)
│   └── agregar_contrasena.sql  agrega la contraseña a una base ya creada
├── videojuegos/
│   ├── gestor_videojuegos.py   CRUD de videojuegos
│   └── Juegos/                 clase padre Videojuego y 5 clases hijas
├── usuarios/
│   ├── usuario.py           clase Usuario (contraseña privada)
│   └── gestor_usuarios.py   crear cuenta e iniciar sesión
└── solicitudes/             compra, intercambio y donación (siguiente fase)
```

## POO

- **Clase y objeto:** Videojuego es la clase; cada juego registrado es un objeto.
- **Herencia:** JuegoAventura, JuegoCompetitivo, JuegoTerror, JuegoEducativo y JuegoDisparos heredan de Videojuego.
- **Encapsulamiento:** el precio es privado (`__precio`); se lee con `obtener_precio()` y se cambia con `cambiar_precio()`, que no acepta negativos. La contraseña del usuario también es privada (`__contrasena`) y se revisa con `verificar_contrasena()`.
- **Polimorfismo:** cada clase hija tiene su propio `jugar()`.
- **CRUD:** el gestor tiene `agregar` (INSERT), `listar_todos` y `buscar` (SELECT), `actualizar` (UPDATE) y `eliminar` (DELETE).
