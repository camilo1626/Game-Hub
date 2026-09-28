import tkinter as tk
from tkinter import ttk

from interfaz import estilos, pantalla_catalogo, pantalla_mis_juegos, pantalla_solicitudes, pantalla_usuarios
from usuarios.usuario import Usuario
from usuarios.gestor_usuarios import GestorUsuarios
from videojuegos.gestor_videojuegos import GestorVideojuegos
from solicitudes.gestor_solicitudes import GestorSolicitudes


class AppGameHub:

    def __init__(self):
        self.gestor_usuarios = GestorUsuarios()
        self.gestor_videojuegos = GestorVideojuegos()
        self.gestor_solicitudes = GestorSolicitudes()
        self.usuario_actual = None
        self.usuarios = []
        self.pantalla_actual = pantalla_usuarios

        self.ventana = tk.Tk()
        self.ventana.title("GameHub circular")
        self.ventana.geometry("1050x680")
        estilos.aplicar_estilos(self.ventana)

        menu = tk.Frame(self.ventana, bg=estilos.PANEL, width=210)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)
        tk.Label(menu, text="GameHub", bg=estilos.PANEL, fg=estilos.TEXTO, font=("Arial", 18, "bold")).pack(pady=(25, 0))
        tk.Label(menu, text="circular", bg=estilos.PANEL, fg=estilos.MORADO, font=("Arial", 12, "bold")).pack(pady=(0, 20))

        estilos.boton(menu, "Catálogo", estilos.TARJETA, lambda: self.abrir(pantalla_catalogo)).pack(fill="x", padx=15, pady=4)
        estilos.boton(menu, "Publicar / Mis juegos", estilos.TARJETA, lambda: self.abrir(pantalla_mis_juegos)).pack(fill="x", padx=15, pady=4)
        estilos.boton(menu, "Solicitudes", estilos.TARJETA, lambda: self.abrir(pantalla_solicitudes)).pack(fill="x", padx=15, pady=4)
        estilos.boton(menu, "Usuarios", estilos.TARJETA, lambda: self.abrir(pantalla_usuarios)).pack(fill="x", padx=15, pady=4)

        tk.Label(menu, text="Usuario actual", bg=estilos.PANEL, fg=estilos.SUAVE).pack(pady=(30, 3))
        self.combo_usuario = ttk.Combobox(menu, state="readonly", width=20)
        self.combo_usuario.pack(padx=15)
        self.combo_usuario.bind("<<ComboboxSelected>>", lambda evento: self.cambiar_usuario())

        self.contenido = tk.Frame(self.ventana, bg=estilos.FONDO, padx=20, pady=10)
        self.contenido.pack(side="left", fill="both", expand=True)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.usuarios = []
        nombres = []
        for fila in self.gestor_usuarios.listar():
            self.usuarios.append(Usuario(fila[1], fila[2], fila[3], fila[0]))
            nombres.append(fila[1])
        self.combo_usuario["values"] = nombres
        if self.usuario_actual is None and len(self.usuarios) > 0:
            self.combo_usuario.current(0)
            self.cambiar_usuario()

    def cambiar_usuario(self):
        posicion = self.combo_usuario.current()
        self.usuario_actual = self.usuarios[posicion]
        self.abrir(pantalla_catalogo)

    def abrir(self, pantalla):
        if self.usuario_actual is None:
            pantalla = pantalla_usuarios
        self.pantalla_actual = pantalla
        for elemento in self.contenido.winfo_children():
            elemento.destroy()
        pantalla.crear(self.contenido, self)

    def recargar(self):
        self.abrir(self.pantalla_actual)

    def iniciar(self):
        self.ventana.mainloop()


def iniciar_interfaz():
    app = AppGameHub()
    app.iniciar()
