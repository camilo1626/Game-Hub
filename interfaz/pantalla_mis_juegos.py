import tkinter as tk
from tkinter import messagebox, simpledialog

from basededatos.conexion import obtener_opciones
from interfaz.estilos import titulo, tarjeta, campo, boton, tabla, TARJETA, VERDE, MORADO, ROJO
from videojuegos.Juegos.tipos import TIPOS
from videojuegos.Juegos.videojuego import Videojuego


def crear(padre, app):
    titulo(padre, "Mis juegos")
    formulario = tarjeta(padre)

    nombre = campo(formulario, "Nombre", 0)
    tipo = campo(formulario, "Tipo", 1, list(TIPOS.keys()))
    genero = campo(formulario, "Género", 2, obtener_opciones("generos"))
    plataforma = campo(formulario, "Plataforma", 3, obtener_opciones("plataformas"))
    desarrollador = campo(formulario, "Desarrollador", 4, obtener_opciones("desarrolladores"))
    anio = campo(formulario, "Año", 5)
    precio = campo(formulario, "Precio (0 si no es venta)", 6)
    estado = campo(formulario, "Estado", 7, Videojuego.Estados)
    oferta = campo(formulario, "Oferta", 8, Videojuego.Ofertas)

    lista = tabla(padre, ("Juego", "Tipo", "Plataforma", "Oferta", "Precio", "Estado"))
    juegos = app.gestor_videojuegos.listar_por_usuario(app.usuario_actual.id_usuario)
    for juego in juegos:
        lista.insert("", "end", values=(juego.nombre, type(juego).__name__, juego.obtener_plataforma(),
                                        juego.obtener_tipo_oferta(), juego.obtener_precio(),
                                        juego.obtener_estado()))

    def publicar():
        if nombre.get() == "" or tipo.get() == "" or estado.get() == "" or oferta.get() == "":
            messagebox.showwarning("GameHub", "Llene todos los campos")
            return
        if not anio.get().isdigit() or not precio.get().isdigit():
            messagebox.showwarning("GameHub", "El año y el precio deben ser números")
            return

        clase = TIPOS[tipo.get()]
        juego = clase(nombre.get(), genero.get(), plataforma.get(), int(anio.get()), int(precio.get()),
                      desarrollador.get(), estado.get(), oferta.get(), app.usuario_actual.id_usuario)
        app.gestor_videojuegos.agregar(juego)
        messagebox.showinfo("GameHub", "Juego publicado")
        app.recargar()

    def seleccionado():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("GameHub", "Seleccione un juego de la tabla")
            return None
        return juegos[lista.index(seleccion[0])]

    def cambiar_precio():
        juego = seleccionado()
        if juego is None:
            return
        nuevo = simpledialog.askinteger("GameHub", "Nuevo precio:")
        if nuevo is None:
            return
        try:
            juego.cambiar_precio(nuevo)
        except ValueError as error:
            messagebox.showerror("GameHub", str(error))
            return
        app.gestor_videojuegos.actualizar(juego)
        app.recargar()

    def eliminar():
        juego = seleccionado()
        if juego:
            app.gestor_videojuegos.eliminar(juego.obtener_id_videojuego())
            app.recargar()

    botones = tk.Frame(formulario, bg=TARJETA)
    botones.grid(row=0, column=2, rowspan=9, padx=20, sticky="n")
    boton(botones, "Publicar", VERDE, publicar).pack(fill="x", pady=3)
    boton(botones, "Cambiar precio", MORADO, cambiar_precio).pack(fill="x", pady=3)
    boton(botones, "Eliminar", ROJO, eliminar).pack(fill="x", pady=3)
