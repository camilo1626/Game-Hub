import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from basededatos.conexion import obtener_opciones
from interfaz.estilos import FONDO, TARJETA, TEXTO, SUAVE, MORADO, VERDE, boton
from solicitudes.solicitud import Solicitud

COLORES_OFERTA = {
    "Venta": ("#2a2370", "#c9c2ff"),
    "Intercambio": ("#5a1a2a", "#ffb3c1"),
    "Donación": ("#12402e", "#8ff0c0"),
}


def crear(padre, app):
    tk.Label(padre, text="Catálogo", bg=FONDO, fg=TEXTO, font=("Arial", 22, "bold")).pack(anchor="w")
    tk.Label(padre, text="Videojuegos con segunda vida", bg=FONDO, fg=SUAVE, font=("Arial", 12)).pack(anchor="w")

    filtros = tk.Frame(padre, bg=FONDO)
    filtros.pack(anchor="w", pady=12)
    plataforma = ttk.Combobox(filtros, values=["Todas las plataformas"] + obtener_opciones("plataformas"),
                              state="readonly", width=25)
    plataforma.current(0)
    plataforma.pack(side="left", padx=(0, 10))
    genero = ttk.Combobox(filtros, values=["Todos los géneros"] + obtener_opciones("generos"),
                          state="readonly", width=25)
    genero.current(0)
    genero.pack(side="left")

    zona = tk.Frame(padre, bg=FONDO)
    zona.pack(fill="both", expand=True)

    juegos = app.gestor_videojuegos.listar_catalogo(app.usuario_actual.id_usuario)

    def solicitar(juego):
        juego.jugar()
        ofrecido = None
        if juego.obtener_tipo_oferta() == "Intercambio":
            ofrecido = simpledialog.askstring("Intercambio", "¿Qué juego ofreces a cambio de " + juego.nombre + "?")
            if not ofrecido:
                return
        elif not messagebox.askyesno("GameHub", "¿Solicitar " + juego.nombre + "?"):
            return
        solicitud = Solicitud(juego.obtener_id_videojuego(), app.usuario_actual.id_usuario, ofrecido)
        app.gestor_solicitudes.agregar(solicitud)
        messagebox.showinfo("GameHub", "Solicitud enviada a " + juego.nombre_dueno)

    def texto_oferta(juego):
        if juego.obtener_tipo_oferta() == "Venta":
            precio = f"{int(juego.obtener_precio()):,}".replace(",", ".")
            return "Venta $" + precio
        return juego.obtener_tipo_oferta()

    def mostrar_tarjetas(evento=None):
        for elemento in zona.winfo_children():
            elemento.destroy()

        posicion = 0
        for juego in juegos:
            if plataforma.current() > 0 and juego.obtener_plataforma() != plataforma.get():
                continue
            if genero.current() > 0 and juego.obtener_genero() != genero.get():
                continue

            tarjeta = tk.Frame(zona, bg=TARJETA, padx=18, pady=14, width=240, height=170)
            tarjeta.grid(row=posicion // 3, column=posicion % 3, padx=8, pady=8)
            tarjeta.grid_propagate(False)

            tk.Label(tarjeta, text=juego.nombre, bg=TARJETA, fg=TEXTO, font=("Arial", 14, "bold"),
                     wraplength=200, justify="left").grid(row=0, column=0, sticky="w")
            tk.Label(tarjeta, text=juego.obtener_plataforma() + " · " + juego.obtener_genero(),
                     bg=TARJETA, fg=SUAVE, font=("Arial", 10)).grid(row=1, column=0, sticky="w")

            fondo, letra = COLORES_OFERTA.get(juego.obtener_tipo_oferta(), (MORADO, TEXTO))
            tk.Label(tarjeta, text=texto_oferta(juego), bg=fondo, fg=letra, font=("Arial", 11, "bold"),
                     padx=10, pady=3).grid(row=2, column=0, sticky="w", pady=8)

            tk.Label(tarjeta, text="De: " + juego.nombre_dueno, bg=TARJETA, fg=SUAVE,
                     font=("Arial", 9)).grid(row=3, column=0, sticky="w")
            boton(tarjeta, "Solicitar", MORADO, lambda j=juego: solicitar(j)).grid(row=4, column=0, sticky="w", pady=(6, 0))
            posicion += 1

        if posicion == 0:
            tk.Label(zona, text="No hay videojuegos disponibles", bg=FONDO, fg=SUAVE,
                     font=("Arial", 12)).grid(row=0, column=0, pady=20)

    plataforma.bind("<<ComboboxSelected>>", mostrar_tarjetas)
    genero.bind("<<ComboboxSelected>>", mostrar_tarjetas)
    mostrar_tarjetas()

    total = app.gestor_videojuegos.contar_reutilizados()
    tk.Label(padre, text=str(total) + " juegos reutilizados", bg=FONDO, fg=VERDE,
             font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
